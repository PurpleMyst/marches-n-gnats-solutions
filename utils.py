import argparse
import sys
import unicodedata
from contextlib import suppress
from functools import lru_cache
from string import ascii_lowercase
from typing import Counter, Literal, NamedTuple, Self

import numpy as np
import pretty_errors as _
import pyperclip
from tqdm import tqdm

import mill

LETTERS = set(ascii_lowercase) | set("äöõü") | set("-")
GREEN = "\x1b[32m"
RED = "\x1b[5;31m"
YELLOW = "\x1b[5;33m"


class _Same:
    __slots__ = ()


SAME = _Same()


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


class Program:
    def __init__(self) -> None:
        self._transitions = []

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

    def __exit__(self, *_) -> None:
        argparser = argparse.ArgumentParser(
            description="Run a Turing machine with the given transition rules."
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
        args = argparser.parse_args()

        transitions = sorted(set(self._transitions))

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
        parsed_rules = mill.parse_transition_rules(rules)
        pyperclip.copy(rules)

        output = []
        with suppress(KeyboardInterrupt):
            f = sys.stdin if args.input == "-" else open(args.input)
            d = f.read()
            x = []
            y = []
            for line in tqdm(d.splitlines(), desc="Processing", unit="line") if args.quiet else d.splitlines():
                if " => " in line:
                    line, expected_output = line.split(" => ", 1)
                else:
                    expected_output = None

                logic_mill = mill.LogicMill(parsed_rules)
                result, steps = logic_mill.run(line.strip(), verbose=not args.quiet)
                output.append(
                    (
                        line,
                        result,
                        steps,
                        len(logic_mill._parse_transitions_list(parsed_rules, "INIT", "HALT")),
                        expected_output,
                    )
                )
                x.append(len(result.strip()))
                y.append(steps)

        for line, result, steps, state_count, expected_output in output:
            print(f"\x1b[1mInput tape\x1b[0m: {line.strip()}{f' ({line.strip().count("|")})' if set(line.strip()) == {'|'} else ''}")
            print(f"\x1b[1mOutput tape\x1b[0m: {result.strip()}{f' ({len(result.strip())})' if set(result.strip()) == {'|'} else ''}")
            print(f"\x1b[1mSteps taken\x1b[0m: {steps:_}")
            print(f"\x1b[1mRule count\x1b[0m: {len(parsed_rules)}")
            print(
                f"\x1b[1mRule size\x1b[0m: {GREEN if len(rules) <= 170000 else RED}{len(rules):_} ({len(rules) / 170000:.2%})\x1b[0m"
            )
            print(
                f"\x1b[1mState count\x1b[0m: {GREEN if state_count <= 1024 else YELLOW if state_count <= 2**16 else RED}{state_count}\x1b[0m"
            )
            print(
                f"\x1b[1mExpected output\x1b[0m: {GREEN if expected_output and expected_output.strip() == result.strip() else RED}{expected_output.strip() if expected_output else 'N/A'}\x1b[0m"
            )
            print()

        x = np.array(x)
        y = np.array(y)

        best_deg = None
        best_err = float("inf")
        best_poly = None

        for deg in range(1, 5):
            coeffs = np.polyfit(x, y, deg)
            p = np.poly1d(coeffs)
            # err = mean_squared_error(y, p(x))
            err = np.mean((y - p(x)) ** 2)
            print(f"deg={deg}, mse={err:.4f}")
            if err < best_err:
                best_err = err
                best_deg = deg
                best_poly = p

        print(best_poly)

    def __call__(
        self,
        from_state: str,
        symbol: str | set[str],
        to_state: str,
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
                    to_state=to_state,
                    new_symbol=sym if isinstance(new_symbol, _Same) else new_symbol,
                    direction=dir,
                )
                self._transitions.append(transition)
        else:
            transition = Transition(
                from_state=from_state,
                symbol=symbol,
                to_state=to_state,
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
