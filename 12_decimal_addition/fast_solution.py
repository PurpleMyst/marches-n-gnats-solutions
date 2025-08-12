from string import ascii_lowercase, digits

from utils import Program

# On the input tape, you'll get two non-negative decimal numbers separated by
# `+` sign. Your task is to compute the sum of these two numbers.
# For example, if the input tape is `2+5`, your output tape should be `7`.
# ---------------------------------------------------------------------------
# Faster solution by processing two digits at a time whenever possible.

PROCESSED_DIGITS = ascii_lowercase
MAX_SUM = 9 + 9


def main() -> None:
    with Program() as p:
        for digit in digits:
            p.ignore("INIT", digit, "R")
            p.ignore("INIT", "+", "R")
            p("INIT", "_", "POP_DIGIT", "_", "L")
            p("POP_DIGIT", digit, f"GOT_DIGIT_{digit}", "_", "L")

            for other_digit in digits:
                p(f"GOT_DIGIT_{digit}", other_digit, f"GOT_DIGITS_{digit}_{other_digit}", "_", "L")

            p("POP_DIGIT", "+", "CONVERT_BACK", "_", "L")

            p(f"GOT_DIGIT_{digit}", "+", f"ADD_DIGIT_{digit}", "+", "L")
            for other_digit in digits:
                p(f"GOT_DIGITS_{digit}_{other_digit}", "+", f"ADD_DIGITS_{digit}_{other_digit}", "+", "L")

            for other_digit in digits:
                for third_digit in digits:
                    p.ignore(f"GOT_DIGITS_{digit}_{other_digit}", third_digit, "L")

                p(
                    f"ADD_DIGIT_{digit}",
                    other_digit,
                    "INIT",
                    PROCESSED_DIGITS[int(digit) + int(other_digit)],
                    "R",
                )
                for third_digit in digits:
                    p(
                        f"ADD_DIGITS_{digit}_{other_digit}",
                        third_digit,
                        f"ADD_DIGIT_{other_digit}",
                        PROCESSED_DIGITS[int(digit) + int(third_digit)],
                        "L",
                    )

            p(f"ADD_DIGIT_{digit}", "_", "INIT", PROCESSED_DIGITS[int(digit)], "R")
            for other_digit in digits:
                p(f"ADD_DIGITS_{digit}_{other_digit}", "_", f"ADD_DIGIT_{other_digit}", PROCESSED_DIGITS[int(digit)], "L")

            for i, other_digit in enumerate(PROCESSED_DIGITS[: MAX_SUM + 1]):
                p.ignore("INIT", other_digit, "R")
                p.ignore(f"ADD_DIGIT_{digit}", other_digit, "L")
                for third_digit in digits:
                    p.ignore(f"ADD_DIGITS_{digit}_{third_digit}", other_digit, "L")

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
