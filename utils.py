import argparse
import sys
from contextlib import suppress
from string import ascii_lowercase
from typing import Counter, Literal, NamedTuple, Self

import pyperclip

import mill

LETTERS = set(ascii_lowercase) | set("äöõü") | set("-")


class Transition(NamedTuple):
    """Represents a transition in a Turing machine."""

    from_state: str
    symbol: str
    to_state: str
    new_symbol: str
    direction: Literal["L", "R"]


class Program:
    def __init__(self) -> None:
        self._transitions = []

    @staticmethod
    def _encode(n: int) -> str:
        """Encodes a number into a string using a custom base-94 encoding."""
        chars = "".join(chr(i) for i in range(33, 127) if chr(i) != "/")
        base = len(chars)
        s = ""
        while n:
            s = chars[n % base] + s
            n //= base
        return s or chars[0]

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
                logic_mill = mill.LogicMill(parsed_rules)
                result, steps = logic_mill.run(line.strip(), verbose=True)
                output.append((line, result, steps, len(parsed_rules)))

        for line, result, steps, len_parsed_rules in output:
            print(f"Input tape: {line.strip()}")
            print(f"Output tape: {result}")
            print(f"Steps taken: {steps}")
            print(f"Rule count: {len_parsed_rules}")
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
