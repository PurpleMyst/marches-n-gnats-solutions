from string import ascii_lowercase

from utils import Program

LETTERS = set(ascii_lowercase) | set("äöõü") | set("-")


def main() -> None:
    with Program() as p:
        for letter in LETTERS:
            p("INIT", letter, f"STEP", letter, "R")
            p("STEP", letter, f"CR_{letter}", "*", "L")

            p(f"CR_{letter}", "_", f"CR_{letter}", "_", "L")

            for other_letter in LETTERS:
                p(f"CR_{letter}", other_letter, f"ADD_{letter}", other_letter, "L")
                p(f"ADD_{letter}", other_letter, f"ADD_{letter}", other_letter, "L")

            p(f"ADD_{letter}", "_", f"RFIND", letter, "L")

            p("RFIND", letter, "RFIND", letter, "R")

        p("STEP", "_", "HALT", "_", "L")
        p("RFIND", "_", "RFIND", "_", "R")
        p("RFIND", "*", "STEP", "_", "R")


if __name__ == "__main__":
    main()
