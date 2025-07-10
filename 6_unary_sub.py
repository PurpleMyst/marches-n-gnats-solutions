from utils import Program

MAX_N = 1000


def main() -> None:
    with Program() as p:
        p("INIT", "|", "COUNT1", "_", "R")
        for n in range(1, MAX_N):
            p(f"COUNT{n}", "|", f"COUNT{n + 1}", "_", "R")
            p(f"COUNT{n}", "-", f"SUB{n}", "_", "R")

            if n - 1 > 0:
                p(f"SUB{n}", "|", f"SUB{n - 1}", "_", "R")
            else:
                p(f"SUB{n}", "|", f"HALT", "_", "R")

            if n - 1 > 0:
                p(f"SUB{n}", "_", f"SUB{n - 1}", "|", "R")
            else:
                p(f"SUB{n}", "_", f"HALT", "|", "R")

        # p("FIND", "|", "FIND", "|", "R")
        #
        # p("FIND", "-", "COUNT0", "_", "R")
        #
        # for n in range(1, MAX_N + 1):
        #     p(f"COUNT{n-1}", "|", f"COUNT{n}", "_", "R")
        #     p(f"COUNT{n}", "_", f"DOSUB{n}", "_", "L")
        #
        #     p(f"DOSUB{n}", "_", f"DOSUB{n}", "_", "L")
        #
        #     if n - 1 != 0:
        #         p(f"DOSUB{n}", "|", f"DOSUB{n-1}", "_", "L")
        #     else:
        #         p(f"DOSUB{n}", "|", f"HALT", "_", "L")


if __name__ == "__main__":
    main()
