from string import digits

from utils import Program

# Shorter solution by just doing two very simple operations: decrement the rhs, increment the lhs,
# stop when the rhs is 0.


def main() -> None:
    with Program() as p:
        for digit in digits:
            p.ignore("INIT", digit, "R")
            p.ignore("INIT", "+", "R")
            p("INIT", "_", "DEC", "_", "L")

            if digit != "0":
                p("DEC", digit, "BACK", str(int(digit) - 1), "L")
            else:
                p("DEC", digit, "DEC", "9", "L")

            p.ignore("BACK", digit, "L")

            p("BACK", "+", "INC", "+", "L")

            if digit != "9":
                p("INC", digit, "INIT", str(int(digit) + 1), "R")
            else:
                p("INC", digit, "INC", "0", "L")
            p("INC", "_", "INIT", "1", "R")

            p("DEC", "+", "FINISH", "_", "R")
            p("FINISH", "9", "FINISH", "_", "R")
            p("FINISH", "_", "HALT", "_", "R")


if __name__ == "__main__":
    main()
