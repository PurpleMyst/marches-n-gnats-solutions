from utils import Program

# On the input tape, you'll get a binary number. Your task is to increment it by 1.
# For example, if the input tape is `1010`, your output tape should be `1011`.
# The output tape shouldn't contain leading zeros (e.g., `001` should be `1`).


def main() -> None:
    with Program() as p:
        for c in "01":
            p.ignore("INIT", c, "R")

        p("INIT", "_", "CARRY", "_", "L")
        p("CARRY", "0", "HALT", "1", "L")
        p("CARRY", "1", "CARRY", "0", "L")
        p("CARRY", "_", "HALT", "1", "L")


if __name__ == "__main__":
    main()
