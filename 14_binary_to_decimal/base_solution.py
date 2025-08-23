from utils import Program
from string import digits

# On the input tape, you'll get a non-negative binary number.Your task is to convert it to a decimal
# number. For example, if the input tape is `1010`, your output tape should be `10`.

BITS = set("01")
OUT = "@"  # marker for the output section

def main() -> None:
    with Program() as p:
        p.find("INIT", "_", BITS, "R", "INIT2", OUT, "R")
        p("INIT2", "_", "NEXT_BIT", "0", "L")
        p.find("NEXT_BIT", "_", {*BITS, OUT}, "L", "GET_BIT", "_", "R")
        p("GET_BIT", OUT, "HALT", "_", "R")

        p("GET_BIT", "0", "DOUBLE", "_", "R")
        p("GET_BIT", "1", "DOUBLE_CARRY", "_", "R")

        p.find("DOUBLE", "_", {*BITS, *digits, OUT}, "R", "DO_DOUBLE", "_", "L")
        p.find("DOUBLE_CARRY", "_", {*BITS, *digits, OUT}, "R", "DO_DOUBLE_CARRY", "_", "L")

        for d in digits:
            if int(d) * 2 < 10:
                assert int(d) * 2 + 1 < 10
                p("DO_DOUBLE", d, "DO_DOUBLE", str((int(d) * 2) % 10), "L")
                p("DO_DOUBLE_CARRY", d, "DO_DOUBLE", str(int(d) * 2 + 1), "L")
            else:
                p("DO_DOUBLE", d, "DO_DOUBLE_CARRY", str((int(d) * 2) % 10), "L")
                p("DO_DOUBLE_CARRY", d, "DO_DOUBLE_CARRY", str((int(d) * 2 + 1) % 10), "L")

            p("DO_DOUBLE", OUT, "NEXT_BIT", OUT, "L")
            p("DO_DOUBLE_CARRY", OUT, "SHIFT_AND_CARRY", OUT, "R")

        p.find("SHIFT_AND_CARRY", "_", {*digits, OUT}, "R", "DO_SHIFT_AND_CARRY", "_", "L")
        for d in digits:
            p("DO_SHIFT_AND_CARRY", d, f"PLOP_{d}", "_", "R")
            p(f"PLOP_{d}", "_", "DO_SHIFT_AND_CARRY_NEXT", d, "L")
        p("DO_SHIFT_AND_CARRY_NEXT", "_", "DO_SHIFT_AND_CARRY", "_", "L")
        p("DO_SHIFT_AND_CARRY", OUT, "PLACE_ONE", OUT, "R")
        p("PLACE_ONE", "_", "NEXT_BIT", "1", "L")




if __name__ == "__main__":
    main()
