from functools import partial

from utils import Program


def main() -> None:
    p = Program()

    p("INIT", "|", "I_1", "_", "R")
    for n in range(1, 100):
        p(f"I_{n}", "|", f"I_{n + 1}", "_", "R")

        p(f"I_{n}", ":", f"D_{n}", "_", "R")

        if n != 1:
            p(f"D_{n}", "|", f"D_{n}", "_", "R")
        else:
            p(f"D_{n}", "|", f"D_{n}", "|", "R")

        p(f"D_{n}", "_", f"HALT", "_", "R")  # failsafe

        if n - 1 != 0:
            p(f"D_{n}", ",", f"D_{n - 1}", "_", "R")
        else:
            p(f"D_{n}", ",", f"E", "_", "R")

    p(f"E", "|", f"E", "_", "R")
    p(f"E", ",", f"K", "_", "R")
    p(f"E", "_", f"HALT", "_", "R")

    p(f"K", ",", f"K", "_", "R")
    p(f"K", "|", f"K", "_", "R")
    p(f"K", "_", f"HALT", "_", "R")


if __name__ == "__main__":
    main()
