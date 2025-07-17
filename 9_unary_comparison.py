from utils import Program

MAX_N = 256

def main() -> None:
    with Program() as p:
        p("INIT", "|", "LHS_1", "|", "R")

        for n in range(1, MAX_N):
            p(f"LHS_{n}", "|", f"LHS_{n + 1}", "|", "R")

        for n in range(1, MAX_N + 1):
            p(f"LHS_{n}", ",", f"RHS_{n}", ",", "R")

        for n in range(1, MAX_N + 1):
            p(f"RHS_{n}", "|", f"RHS_{n - 1}", "|", "R")

        p(f"RHS_{0}", "|", f"LT", "|", "L")
        p(f"RHS_{0}", "_", f"EQ", "_", "L")

        for n in range(1, MAX_N + 1):
            p(f"RHS_{n}", "_", f"GT", "_", "L")

        p.ignore("LT", "|", "L")
        p.ignore("GT", "|", "L")
        p.ignore("EQ", "|", "L")

        p("LT", ",", "HALT", "<", "R")
        p("GT", ",", "HALT", ">", "R")
        p("EQ", ",", "HALT", "=", "R")


if __name__ == "__main__":
    main()
