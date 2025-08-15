from utils import LETTERS, Program

MAX_N = 800
LETTERS &= set("-Nabdefghijklmnoprstuwyäõöü")


def main() -> None:
    with Program() as p:
        for l in LETTERS:
            p("INIT", l, "INIT", "_", "R")
        p("INIT", "+", "COUNT_1", "_", "R")
        p("INIT", "_", "HALT", "|", "L")

        for n in range(1, MAX_N + 1):
            for l in LETTERS:
                p(f"COUNT_{n}", l, f"COUNT_{n}", "_", "R")
            p(f"COUNT_{n}", "+", f"COUNT_{n + 1}", "_", "R")

            p(f"COUNT_{n}", "_", f"COUNT_{n - 1}", "|", "R")

        p(f"COUNT_0", "_", "HALT", "|", "R")
