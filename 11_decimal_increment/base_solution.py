from string import digits
from utils import Program


def main() -> None:
    with Program() as p:
        for number in digits:
            p("INIT", number, "FIND_EDGE", number, "R")
            p.ignore("FIND_EDGE", number, "R")
            p("FIND_EDGE", "_", "INCREMENT", "_", "L")

            if number != "9":
                p("INCREMENT", number, "HALT", str(int(number) + 1), "L")
            else:
                p("INCREMENT", number, "INCREMENT", "0", "L")

        p("INCREMENT", "_", "HALT", "1", "L")

if __name__ == "__main__":
    main()
