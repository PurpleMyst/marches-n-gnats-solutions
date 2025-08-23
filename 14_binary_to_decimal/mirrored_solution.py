from utils import Program
from string import digits

# On the input tape, you'll get a non-negative binary number.Your task is to convert it to a decimal
# number. For example, if the input tape is `1010`, your output tape should be `10`.

BITS = set("01")
OUT = "@"  # marker for the output section

def main() -> None:
    with Program() as p:
        for b in BITS:
            p("INIT", b, "INIT2", b, "L")
        p("INIT2", "_", "INIT3", OUT, "L")
        p("INIT3", "_", "INIT4", "0", "R")
        p.find("INIT4", "_", {*BITS, OUT}, "R", "INIT5", "E", "L")
        p.find("INIT5", OUT, BITS, "L", "GET_BIT", OUT, "R")
        p.find("TO_INPUT", OUT, set(digits), "R", "GET_BIT", OUT, "R")

        p.ignore("GET_BIT", "_", "R")
        p("GET_BIT", "0", "DOUBLE", "_", "L")
        p("GET_BIT", "1", "DOUBLE_CARRY", "_", "L")
        p("GET_BIT", "E", "REMOVE_OUT", "_", "L")
        p.find("REMOVE_OUT", OUT, "_", "L", "HALT", "_", "L")

        p.find("DOUBLE", OUT, {*digits, "_"}, "L", "DO_DOUBLE", OUT, "L")
        p.find("DOUBLE_CARRY", OUT, {*digits, "_"}, "L", "DO_DOUBLE_CARRY", OUT, "L")

        for d in digits:
            if int(d) * 2 < 10:
                assert int(d) * 2 + 1 < 10
                p("DO_DOUBLE", d, "DO_DOUBLE", str((int(d) * 2) % 10), "L")
                p("DO_DOUBLE_CARRY", d, "DO_DOUBLE", str(int(d) * 2 + 1), "L")
            else:
                p("DO_DOUBLE", d, "DO_DOUBLE_CARRY", str((int(d) * 2) % 10), "L")
                p("DO_DOUBLE_CARRY", d, "DO_DOUBLE_CARRY", str((int(d) * 2 + 1) % 10), "L")

            p("DO_DOUBLE", "_", "TO_INPUT", "_", "R")
            p("DO_DOUBLE_CARRY", "_", "TO_INPUT", "1", "R")




if __name__ == "__main__":
    main()
