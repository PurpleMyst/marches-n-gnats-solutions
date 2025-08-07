from string import digits, ascii_lowercase
from utils import Program

# On the input tape, you'll get two non-negative decimal numbers separated by
# `+` sign. Your task is to compute the sum of these two numbers.
# For example, if the input tape is `2+5`, your output tape should be `7`.
# ---------------------------------------------------------------------------
# "Simple", or at least general, solution: we keep track of which digits we've already processed by
# utilizing a different alphabet for them, i.e. ascii letters, which also allows us to do two passes
# over our data: one where we just add digit-by-digit, ignoring carry, and another where we take
# care of the conversion back to regular digits with carry.

PROCESSED_DIGITS = ascii_lowercase
MAX_SUM = 9 + 9

def main() -> None:
    with Program() as p:
        for digit in digits:
            p.ignore("INIT", digit, "R")
            p.ignore("INIT", "+", "R")
            p("INIT", "_", "POP_DIGIT", "_", "L")
            p("POP_DIGIT", digit, f"GOT_DIGIT_{digit}", "_", "L")
            p("POP_DIGIT", "+", "CONVERT_BACK", "_", "L")
            p(f"GOT_DIGIT_{digit}", "+", f"ADD_DIGIT_{digit}", "+", "L")
            p.ignore(f"ADD_DIGIT_{digit}", "*", "L")

            for other_digit in digits:
                p.ignore(f"GOT_DIGIT_{digit}", other_digit, "L")
                p(f"ADD_DIGIT_{digit}", other_digit, "INIT", PROCESSED_DIGITS[int(digit) + int(other_digit)], "R")

            p(f"ADD_DIGIT_{digit}", "_", "INIT", PROCESSED_DIGITS[int(digit)], "R")

            for i, other_digit in enumerate(PROCESSED_DIGITS[:MAX_SUM + 1]):
                p.ignore("INIT", other_digit, "R")
                p.ignore(f"ADD_DIGIT_{digit}", other_digit, "L")

                if i < 10:
                    p("CONVERT_BACK", other_digit, "CONVERT_BACK", str(i), "L")
                else:
                    assert i // 10 == 1
                    p("CONVERT_BACK", other_digit, f"CARRY", str(i % 10), "L")

                if i + 1 < 10:
                    p("CARRY", other_digit, "CONVERT_BACK", str(i + 1), "L")
                else:
                    p("CARRY", other_digit, "CARRY", str((i + 1) % 10), "L")

            p("CONVERT_BACK", digit, "HALT", digit, "L")

            if int(digit) < 9:
                p("CARRY", digit, "HALT", str(int(digit) + 1), "L")
            else:
                p("CARRY", digit, "CARRY", "0", "L")

        p("CARRY", "_", "HALT", "1", "L")
        p("CONVERT_BACK", "_", "HALT", "_", "L")

if __name__ == "__main__":
    main()
