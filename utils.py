import argparse
import re
import sys
import unicodedata
from concurrent.futures import ProcessPoolExecutor
from contextlib import suppress
from functools import lru_cache, partial
from pathlib import Path
from string import ascii_lowercase
from typing import Counter, Literal, NamedTuple, Self

import logic_mill_rs as mill
import pretty_errors as _
import pyperclip
from tqdm import tqdm

LETTERS = set(ascii_lowercase) | set("äöõü") | set("-")
GREEN = "\x1b[32m"
RED = "\x1b[5;31m"
YELLOW = "\x1b[5;33m"


class _Same:
    __slots__ = ()


SAME = _Same()


def is_unary(tape: str) -> bool:
    """Check if the tape is a unary number (only contains '|')"""
    return set(tape) == {"|"}


def count_unary(tape: str) -> int | None:
    """Count the number of '|' characters in a unary tape."""
    return tape.count("|") if is_unary(tape) else None


def base_and_suffix(n: str) -> tuple[str, int | None]:
    """Given a state name like FOO_123, return ("FOO", 123). If there is no suffix, return ("FOO", None)."""
    if m := re.match(r"^(.*)_(\d+)$", n):
        return m.group(1), int(m.group(2))
    return n, None


class Transition(NamedTuple):
    """Represents a transition in a Turing machine."""

    from_state: str
    symbol: str
    to_state: str
    new_symbol: str
    direction: Literal["L", "R"]


@lru_cache(maxsize=1)
def build_safe_charset(use_full_plane: bool = False) -> str:
    """
    Build a deterministic, safe charset for encoding state IDs.
    Excludes:
      - Control characters, separators, combining marks (categories C, Z, M)
      - Characters that are whitespace (.isspace())
      - The slash '/' because '//' is a comment prefix
    Iterates from U+0021 (33) up to U+FFFF by default (BMP), or up to U+10FFFF if
    use_full_plane is True.

    This function is cached (so the scan happens once).
    """
    max_cp = 0x110000 if use_full_plane else 0x10000
    chars = []
    for cp in range(33, max_cp):
        ch = chr(cp)
        if ch == "/":
            continue
        if ch.isspace():
            continue
        cat = unicodedata.category(ch)
        # skip Control/Other (C*), Separator (Z*), and Mark (M*) categories
        if cat[0] in ("C", "Z", "M"):
            continue
        chars.append(ch)

    # Fallback to original printable-ascii-without-slash if something went wrong
    if not chars:
        return "".join(chr(i) for i in range(33, 127) if chr(i) != "/")

    return "".join(chars)


def _do_run(item: tuple[str, str | None], rules: str, quiet: bool):
    line, expected_output = item
    logic_mill = mill.LogicMill(rules)
    result, steps = logic_mill.run(line.strip(), verbose=not quiet)
    return line, expected_output, logic_mill, result, steps


def _do_split(line: str):
    if " => " in line:
        line, expected_output = line.split(" => ", 1)
    else:
        expected_output = None
    return line, expected_output


class Program:
    def __init__(self) -> None:
        self._transitions: list[Transition] = []

    @staticmethod
    def _encode(n: int) -> str:
        if n < 0:
            raise ValueError("n must be >= 0")

        chars = build_safe_charset(use_full_plane=True)
        base = len(chars)
        assert base > 1, "Charset must have at least 2 characters"

        if n == 0:
            return chars[0]

        s = ""
        while n:
            s = chars[n % base] + s
            n //= base
        return s

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type, *_) -> None:
        if exc_type is not None:
            return

        argparser = argparse.ArgumentParser(
            description="Run a Turing machine with the given transition rules.",
            add_help=False,
        )
        argparser.add_argument(
            "-H", "--HELP", action="help", help="Show this help message and exit."
        )
        argparser.add_argument(
            "-i",
            "--input",
            type=str,
            default="-",
            help="Input file containing the tape to process. Use '-' for stdin.",
        )
        argparser.add_argument(
            "-c",
            "--compress",
            action="store_true",
            help="Compress state names to short identifiers.",
        )
        argparser.add_argument(
            "-q",
            "--quiet",
            action="store_true",
            help="Avoid verbose output, only print results.",
        )
        argparser.add_argument(
            "-j",
            "--jobs",
            action="store_true",
            help="Use multiple processes to run the Turing machine on multiple inputs.",
        )
        argparser.add_argument(
            "-n",
            "--number",
            type=int,
            default=None,
            help="Limit the number of lines to process from the input.",
        )
        argparser.add_argument(
            "-s", "--skip", type=int, default=None, help="Skip the first N lines from the input."
        )
        argparser.add_argument(
            "-U", "--no-used", action="store_true", help="Do not compute unused rules."
        )
        argparser.add_argument(
            "-f", "--failing", action="store_true", help="Only show failing cases."
        )
        args = argparser.parse_args()

        transitions = sorted(
            set(self._transitions),
            key=lambda t: (
                base_and_suffix(t.from_state),
                t.symbol,
                base_and_suffix(t.to_state),
                t.new_symbol,
                t.direction,
            ),
        )

        frequency = Counter()
        for transition in transitions:
            if transition.from_state not in ("HALT", "INIT"):
                frequency[transition.from_state] += 1
            if transition.to_state not in ("HALT", "INIT"):
                frequency[transition.to_state] += 1
        sorted_states = sorted(frequency, key=lambda w: frequency[w], reverse=True)
        state_names = {
            state: self._encode(i) if args.compress else state
            for i, state in enumerate(sorted_states)
        }
        for passthru_state in ("INIT", "HALT"):
            assert passthru_state not in state_names
            state_names[passthru_state] = passthru_state

        lines = []
        for transition in transitions:
            from_state = state_names[transition.from_state]
            to_state = state_names[transition.to_state]
            symbol = transition.symbol
            new_symbol = transition.new_symbol
            direction = transition.direction
            lines.append(f"{from_state} {symbol} {to_state} {new_symbol} {direction}")

        rules = "\n".join(lines)
        rules_path = (
            Path("rules.txt") if args.input == "-" else Path(args.input).parent / "rules.txt"
        )
        dot_path = (
            Path("rules.dot") if args.input == "-" else Path(args.input).parent / "rules.dot"
        )
        with open(rules_path, "w", encoding="utf-8") as f:
            f.write(rules)
        pyperclip.copy(rules)
        with open(dot_path, "w", encoding="utf-8") as f:
            f.write("digraph G {\n")
            f.write('  rankdir="LR";\n')
            f.write('  node [shape=circle, fontname="monospace"];\n')
            f.write('  "INIT" [shape=doublecircle, style=filled, fillcolor=lightgrey, rank=min];\n')
            for transition in transitions:
                from_state = transition.from_state
                to_state = transition.to_state
                symbol = transition.symbol
                new_symbol = transition.new_symbol
                direction = transition.direction
                f.write(f'  "{from_state}" -> "{to_state}" [label="{symbol}→{new_symbol},{direction}"];\n')
            f.write('  "HALT" [shape=doublecircle, style=filled, fillcolor=lightgrey, rank=max];\n')
            f.write("}\n")


        output = []

        unused_rules: set[tuple[str, str]] | None = None

        with suppress(KeyboardInterrupt), ProcessPoolExecutor() as executor:
            f = sys.stdin if args.input == "-" else open(args.input, encoding="utf-8")
            d = f.read()
            do_run = partial(_do_run, rules=rules, quiet=args.quiet)
            lines = d.splitlines()
            if args.skip is not None:
                lines = lines[args.skip :]
            if args.number is not None:
                lines = lines[: args.number]
            total = len(lines)
            for line, expected_output, logic_mill, result, steps in (
                tqdm(
                    (executor.map if args.jobs else map)(do_run, map(_do_split, lines)),
                    desc="Processing",
                    unit="line",
                    total=total,
                )
                if args.quiet
                else map(do_run, map(_do_split, lines))
            ):
                output.append(
                    (
                        line,
                        result,
                        steps,
                        logic_mill.state_count(),
                        expected_output,
                    )
                )

                new_unused = set(logic_mill.unused_rules())
                if unused_rules is None:
                    unused_rules = new_unused
                else:
                    unused_rules &= new_unused

        total_steps = 0
        state_count = 0
        had_failing = False
        for line, result, steps, state_count, expected_output in output:
            total_steps += steps

            if (
                args.failing
                and expected_output is not None
                and expected_output.strip() == result.strip()
            ):
                continue
            had_failing = True

            print(
                f"\x1b[1mInput tape\x1b[0m: {line.strip()}{f' ({n})' if (n := count_unary(line.strip())) is not None else ''}"
            )
            print(
                f"\x1b[1mOutput tape\x1b[0m: {result.strip()}{f' ({n})' if (n := count_unary(result.strip())) is not None else ''}"
            )
            print(f"\x1b[1mSteps taken\x1b[0m: {steps:_}")
            expected_output_color = (
                GREEN
                if expected_output is not None and expected_output.strip() == result.strip()
                else RED
            )
            print(
                f"\x1b[1mExpected output\x1b[0m: {expected_output_color}{expected_output.strip() if expected_output is not None else 'N/A'}{f' ({n})' if expected_output is not None and (n := count_unary(expected_output.strip())) is not None else ''}\x1b[0m"
            )
            print()

        if not had_failing and args.failing:
            print(f"{GREEN}All {len(output)} cases passed! \x1b[0m")
            print()

        print(f"\x1b[1mRule count\x1b[0m: {len(rules.splitlines())}")

        rule_size_color = GREEN if len(rules) <= 170_000 else RED
        print(
            f"\x1b[1mRule size\x1b[0m: {rule_size_color}{len(rules):_} ({len(rules) / 170000:.2%})\x1b[0m"
        )
        state_count_color = (
            GREEN if state_count <= 1024 else YELLOW if state_count <= 2**16 else RED
        )
        print(f"\x1b[1mState count\x1b[0m: {state_count_color}{state_count}\x1b[0m")

        print(f"\x1b[1mTotal steps\x1b[0m: {total_steps:_}")
        print(f"\x1b[1mAverage steps\x1b[0m: {total_steps / len(output):_.2f}")

        if unused_rules and not args.no_used and args.skip is None and args.number is None:
            print(f"\n\x1b[1mUnused rules\x1b[0m: {len(unused_rules)}/{len(rules.splitlines())}")
            dedup = {}
            for state, symbol in unused_rules:
                if m := re.match(r"(\w+)_(\d+)$", state):
                    dedup.setdefault((m.group(1), symbol), set()).add(int(m.group(2)))
                else:
                    dedup.setdefault((state, symbol), set()).add(None)
            for state, rules in sorted(dedup.items()):
                print(
                    f"  {state[0]} {state[1]}  " + str(sorted(rules) if None not in rules else "✨")
                )

    def __call__(
        self,
        from_state: str,
        symbol: str | set[str],
        to_state: str | _Same,
        new_symbol: str | _Same,
        dir: Literal["L", "R"],
    ) -> None:
        """Writes a rule to the file in the format:
        from_state current_symbol to_state new_symbol direction
        """
        if isinstance(symbol, set):
            for sym in symbol:
                transition = Transition(
                    from_state=from_state,
                    symbol=sym,
                    to_state=from_state if isinstance(to_state, _Same) else to_state,
                    new_symbol=sym if isinstance(new_symbol, _Same) else new_symbol,
                    direction=dir,
                )
                self._transitions.append(transition)
        else:
            transition = Transition(
                from_state=from_state,
                symbol=symbol,
                to_state=from_state if isinstance(to_state, _Same) else to_state,
                new_symbol=symbol if isinstance(new_symbol, _Same) else new_symbol,
                direction=dir,
            )
            self._transitions.append(transition)

    def ignore(self, state: str, symbol: str | set[str], dir: Literal["L", "R"]) -> None:
        """Writes a rule that ignores the current symbol and stays in the same state."""
        if isinstance(symbol, set):
            for symbol in symbol:
                self(state, symbol, state, symbol, dir)
        else:
            self(state, symbol, state, symbol, dir)

    def find(
        self,
        from_state: str,
        needle: str | set[str],
        ignoring: str | set[str],
        search_dir: Literal["L", "R"],
        to_state: str,
        to_symbol: str | _Same,
        to_dir: Literal["L", "R"] | None = None,
    ) -> None:
        """Write a set of rules which will search for a symbol in the tape, ignoring
        certain symbols, and then transition to a new state with a new symbol and direction."""

        if ignoring:
            self.ignore(from_state, ignoring, search_dir)

        if isinstance(needle, set):
            for n in needle:
                self(
                    from_state,
                    n,
                    to_state,
                    to_symbol,
                    to_dir if to_dir is not None else ("R" if search_dir == "L" else "R"),
                )
        else:
            self(
                from_state,
                needle,
                to_state,
                to_symbol,
                to_dir if to_dir is not None else ("R" if search_dir == "L" else "R"),
            )
