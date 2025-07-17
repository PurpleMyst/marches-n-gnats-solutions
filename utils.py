from typing import Counter, Literal, NamedTuple, Self


class Transition(NamedTuple):
    """Represents a transition in a Turing machine."""

    from_state: str
    symbol: str
    to_state: str
    new_symbol: str
    direction: Literal["L", "R"]


class Program:
    def __init__(self, *, filename: str = "rules.txt", debug: bool = __debug__) -> None:
        self._transitions = []

        self._filename = filename
        self._debug = debug

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
        transitions = sorted(set(self._transitions))

        frequency = Counter()
        for transition in transitions:
            if transition.from_state not in ("HALT", "INIT"):
                frequency[transition.from_state] += 1
            if transition.to_state not in ("HALT", "INIT"):
                frequency[transition.to_state] += 1
        sorted_states = sorted(frequency, key=lambda w: frequency[w], reverse=True)
        state_names = {
            state: self._encode(i) if not self._debug else state
            for i, state in enumerate(sorted_states)
        }
        for passthru_state in ("INIT", "HALT"):
            assert passthru_state not in state_names
            state_names[passthru_state] = passthru_state

        with open(self._filename, "w", newline="\n", encoding="utf-8") as f:
            for transition in transitions:
                from_state = state_names[transition.from_state]
                to_state = state_names[transition.to_state]
                symbol = transition.symbol
                new_symbol = transition.new_symbol
                direction = transition.direction
                f.write(f"{from_state} {symbol} {to_state} {new_symbol} {direction}\n")

    def __call__(
        self, from_: str, symbol: str, to: str, new_symbol: str, dir: Literal["L", "R"]
    ) -> None:
        """Writes a rule to the file in the format:
        from_state current_symbol to_state new_symbol direction
        """
        transition = Transition(
            from_state=from_, symbol=symbol, to_state=to, new_symbol=new_symbol, direction=dir
        )
        self._transitions.append(transition)

    def ignore(self, state: str, symbol: str, dir: Literal["L", "R"]) -> None:
        """Writes a rule that ignores the current symbol and stays in the same state."""
        self(state, symbol, state, symbol, dir)
