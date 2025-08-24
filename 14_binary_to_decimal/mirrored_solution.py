from string import digits

from utils import Program

# On the input tape, you'll get a non-negative binary number.Your task is to convert it to a decimal
# number. For example, if the input tape is `1010`, your output tape should be `10`.

BITS = set("01")
SOO = "@"  # start of output
EOI = "#"  # end of input


def main() -> None:
    with Program() as p:
        # Initialize the tape with markers
        p.find("INIT", "_", BITS, "R", "INIT2", EOI, "L")
        p.find("INIT2", "_", BITS, "L", "INIT3", SOO, "L")
        p("INIT3", "_", "TO_INPUT", "0", "R")

        # Main loop: read bits and double the current output, incrementing if the bit is 1
        p.find("TO_INPUT", SOO, set(digits), "R", "GET_BIT", SOO, "R")
        p.ignore("GET_BIT", "_", "R")
        p("GET_BIT", "0", "DOUBLE", "_", "L")
        p("GET_BIT", "1", "DOUBLE_CARRY", "_", "L")
        p("GET_BIT", EOI, "REMOVE_SOO", "_", "L")
        p.find("REMOVE_SOO", SOO, "_", "L", "HALT", "_", "L")

        p.find("DOUBLE", SOO, {*BITS, "_"}, "L", "DO_DOUBLE", SOO, "L")
        p.find("DOUBLE_CARRY", SOO, {*BITS, "_"}, "L", "DO_DOUBLE_CARRY", SOO, "L")

        for d in digits:
            p(
                "DO_DOUBLE",
                d,
                "DO_DOUBLE_CARRY" if int(d) * 2 >= 10 else "DO_DOUBLE",
                str((int(d) * 2) % 10),
                "L",
            )
            p(
                "DO_DOUBLE_CARRY",
                d,
                "DO_DOUBLE_CARRY" if int(d) * 2 + 1 >= 10 else "DO_DOUBLE",
                str((int(d) * 2) % 10 + 1),
                "L",
            )

            p("DO_DOUBLE", "_", "TO_INPUT", "_", "R")
            p("DO_DOUBLE_CARRY", "_", "TO_INPUT", "1", "R")


if __name__ == "__main__":
    main()
