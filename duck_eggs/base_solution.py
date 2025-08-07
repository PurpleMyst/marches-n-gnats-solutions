import itertools
from typing import NamedTuple, Self

from utils import Program

ALPHABET = "SML"


class State(NamedTuple):
    """State of the program."""
    s: int  # Count of 'S'
    m: int  # Count of 'M'
    l: int  # Count of 'L'

    @classmethod
    def initial(cls) -> Self:
        """Initial state of the program."""
        return cls(0, 0, 0)

    def add(self, char: str) -> Self:
        """Increment the state based on the character."""
        match char:
            case 'S':
                return type(self)(self.s + 1, self.m, self.l)
            case 'M':
                return type(self)(self.s, self.m + 1, self.l)
            case 'L':
                return type(self)(self.s, self.m, self.l + 1)
            case _:
                raise ValueError(f"Invalid character: {char}")

    def sub(self, char: str) -> Self:
        """Decrement the state based on the character."""
        match char:
            case 'S':
                return type(self)(self.s - 1, self.m, self.l)
            case 'M':
                return type(self)(self.s, self.m - 1, self.l)
            case 'L':
                return type(self)(self.s, self.m, self.l - 1)
            case _:
                raise ValueError(f"Invalid character: {char}")


    def __str__(self) -> str:
        return f"{self.s}_{self.m}_{self.l}"

def main() -> None:
    with Program() as p:
        for char in ALPHABET:
            p("INIT", char, f"COUNT_{State.initial().add(char)}", "_", "R")

        for a, b, c in itertools.product(range(16), repeat=3):
            state = State(a, b, c)

            for char in ALPHABET:
                p(f"COUNT_{state}", char, f"COUNT_{state.add(char)}", "_", "R")

            if a != 0:
                p(f"COUNT_{state}", "_", f"DROP_{state.sub('S')}", "S", "R")
                p(f"DROP_{state}", "_", f"DROP_{state.sub('S')}", "S", "R")
            elif b != 0:
                p(f"COUNT_{state}", "_", f"DROP_{state.sub('M')}", "M", "R")
                p(f"DROP_{state}", "_", f"DROP_{state.sub('M')}", "M", "R")
            elif c != 0:
                p(f"COUNT_{state}", "_", f"DROP_{state.sub('L')}", "L", "R")
                p(f"DROP_{state}", "_", f"DROP_{state.sub('L')}", "L", "R")
            else:
                p(f"DROP_{state}", "_", "HALT", "_", "R")




if __name__ == "__main__":
    main()
