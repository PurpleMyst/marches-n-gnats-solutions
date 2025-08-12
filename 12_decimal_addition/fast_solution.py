from string import ascii_lowercase, digits
from itertools import product

from utils import Program

# On the input tape, you'll get two non-negative decimal numbers separated by
# `+` sign. Your task is to compute the sum of these two numbers.
# For example, if the input tape is `2+5`, your output tape should be `7`.
# ---------------------------------------------------------------------------
# Faster solution by processing two digits at a time whenever possible.

PROCESSED_DIGITS = ascii_lowercase
MAX_SUM = 9 + 9
MAX_N = 3
ALLOWED_FINAL_DIGITS = "27"  # Determined via experimentation on what got the fewest steps.


def main() -> None:
    with Program() as p:
        for n in range(1, MAX_N + 1):
            for seq in map("".join, product(digits, repeat=n)):
                if n == MAX_N and seq[-1] not in ALLOWED_FINAL_DIGITS:
                    continue

                p(f"READ_RHS_{seq}", "+", f"ADD_{seq}", "+", "L")

                for digit in digits:
                    p.ignore(f"SKIP_{seq}", digit, "L")
                    if n == MAX_N or (n == MAX_N - 1 and digit not in ALLOWED_FINAL_DIGITS):
                        p(f"READ_RHS_{seq}", digit, f"SKIP_{seq}", digit, "L")
                    else:
                        p(f"READ_RHS_{seq}", digit, f"READ_RHS_{seq + digit}", "_", "L")

                p(f"READ_RHS_{seq}", "+", f"ADD_{seq}", "+", "L")
                p(f"SKIP_{seq}", "+", f"ADD_{seq}", "+", "L")

                for digit in digits:
                    if n == 1:
                        p(
                            f"ADD_{seq}",
                            digit,
                            "INIT",
                            PROCESSED_DIGITS[int(digit) + int(seq)],
                            "R",
                        )
                    else:
                        p(
                            f"ADD_{seq}",
                            digit,
                            f"ADD_{seq[1:]}",
                            PROCESSED_DIGITS[int(digit) + int(seq[0])],
                            "L",
                        )

                if n == 1:
                    p(f"ADD_{seq}", "_", "INIT", PROCESSED_DIGITS[int(seq)], "R")
                else:
                    p(f"ADD_{seq}", "_", f"ADD_{seq[1:]}", PROCESSED_DIGITS[int(seq[0])], "L")

                for processed_digit in PROCESSED_DIGITS[: MAX_SUM + 1]:
                    p.ignore(f"ADD_{seq}", processed_digit, "L")

        for digit in digits:
            p.ignore("INIT", digit, "R")
            p.ignore("INIT", "+", "R")
            p("INIT", "_", "POP_DIGIT", "_", "L")
            p("POP_DIGIT", digit, f"READ_RHS_{digit}", "_", "L")

            p("POP_DIGIT", "+", "CONVERT_BACK", "_", "L")

            for i, other_digit in enumerate(PROCESSED_DIGITS[: MAX_SUM + 1]):
                p.ignore("INIT", other_digit, "R")

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
