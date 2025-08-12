import argparse
import sys
import unicodedata
from contextlib import suppress
from functools import lru_cache
from string import ascii_lowercase
from typing import Counter, Literal, NamedTuple, Self

import pyperclip

import mill

LETTERS = set(ascii_lowercase) | set("äöõü") | set("-")
GREEN = "\x1b[32m"
RED = "\x1b[5;31m"
YELLOW = "\x1b[5;33m"


class Transition(NamedTuple):
    """Represents a transition in a Turing machine."""

    from_state: str
    symbol: str
    to_state: str
    new_symbol: str
    direction: Literal["L", "R"]


@lru_cache(maxsize=1)
def _build_safe_charset(use_full_plane: bool = False) -> str:
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

        chars = _build_safe_charset(use_full_plane=True)
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
            for line in sys.stdin if args.input == "-" else open(args.input):
                if " => " in line:
                    line, expected_output = line.split(" => ", 1)
                else:
                    expected_output = None

                logic_mill = mill.LogicMill(parsed_rules)
                result, steps = logic_mill.run(line.strip(), verbose=True)
                output.append(
                    (
                        line,
                        result,
                        steps,
                        len(logic_mill._parse_transitions_list(parsed_rules, "INIT", "HALT")),
                        expected_output,
                    )
                )

        for line, result, steps, state_count, expected_output in output:
            print(f"\x1b[1mInput tape\x1b[0m: {line.strip()}")
            print(f"\x1b[1mOutput tape\x1b[0m: {result.strip()}")
            print(f"\x1b[1mSteps taken\x1b[0m: {steps}")
            print(f"\x1b[1mRule count\x1b[0m: {len(parsed_rules)}")
            print(
                f"\x1b[1mRule size\x1b[0m: {GREEN if len(rules) <= 170000 else RED}{len(rules)}\x1b[0m"
            )
            print(
                f"\x1b[1mState count\x1b[0m: {GREEN if state_count <= 1024 else YELLOW if state_count <= 2**16 else RED}{state_count}\x1b[0m"
            )
            print(
                f"\x1b[1mExpected output\x1b[0m: {GREEN if expected_output and expected_output.strip() == result.strip() else RED}{expected_output.strip() if expected_output else 'N/A'}\x1b[0m"
            )
            print()

    def __call__(
        self, from_: str, symbol: str, to: str, new_symbol: str, dir: Literal["L", "R"]
    ) -> None:
        """Writes a rule to the file in the format:
        from_state current_symbol to_state new_symbol direction
        """
        transition = Transition(
            from_state=from_,
            symbol=symbol,
            to_state=to,
            new_symbol=new_symbol,
            direction=dir,
        )
        self._transitions.append(transition)

    def ignore(self, state: str, symbol: str, dir: Literal["L", "R"]) -> None:
        """Writes a rule that ignores the current symbol and stays in the same state."""
        self(state, symbol, state, symbol, dir)
