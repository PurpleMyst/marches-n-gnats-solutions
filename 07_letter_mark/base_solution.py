from string import ascii_lowercase

from utils import Program

LETTERS = set(ascii_lowercase) | set("äöõü") | set("-")


def main() -> None:
    with Program() as p:
        for letter in LETTERS:
            p("INIT", letter, f"APPEND_{letter}", "*", "R")

            p("FIND", letter, f"APPEND_{letter}", "*", "R")

            for other_letter in LETTERS | set("[]"):
                if letter == "c" and other_letter == "h":
                    p(f"APPEND_{letter}", other_letter, f"TAKE_ch", "*", "L")
                else:
                    p(f"APPEND_{letter}", other_letter, f"APPEND_{letter}", other_letter, "R")

            p(f"APPEND_{letter}", "_", f"DO_{letter}", "_", "R")

            for other_letter in LETTERS | set("[]"):
                p(f"DO_{letter}", other_letter, f"DO_{letter}", other_letter, "R")

            if letter == "w":
                p(f"DO_{letter}", "_", f"LEFT_w", "[", "R")
                p("LEFT_w", "_", "RIGHT_w", "w", "R")
                p("RIGHT_w", "_", "CARRIAGE_RETURN", "]", "L")
            else:
                p(f"DO_{letter}", "_", f"CARRIAGE_RETURN", letter, "L")

            p(f"CARRIAGE_RETURN", letter, "CARRIAGE_RETURN", letter, "L")

            p(f"NEXT_CHAR", letter, "NEXT_CHAR", letter, "L")

        for letter in "[]":
            p(f"CARRIAGE_RETURN", letter, "CARRIAGE_RETURN", letter, "L")
            p(f"NEXT_CHAR", letter, "NEXT_CHAR", letter, "L")

        for other_letter in LETTERS | set("[]"):
            p(f"APPEND_ch", other_letter, f"APPEND_ch", other_letter, "R")
            p(f"DO_ch", other_letter, f"DO_ch", other_letter, "R")

        p(f"APPEND_ch", "_", f"DO_ch", "_", "R")
        p(f"DO_ch", "_", f"LEFT_ch", "[", "R")
        p(f"LEFT_ch", "_", f"MID_ch", "c", "R")
        p(f"MID_ch", "_", f"RIGHT_ch", "h", "R")
        p(f"RIGHT_ch", "_", f"CARRIAGE_RETURN", "]", "L")

        p("TAKE_ch", "*", "APPEND_ch", "_", "R")
        p("APPEND_ch", "*", "APPEND_ch", "*", "R")
        p(f"CARRIAGE_RETURN", "_", "NEXT_CHAR", "_", "L")
        p(f"FIND", "_", "HALT", "_", "L")
        p(f"NEXT_CHAR", "*", "FIND", "_", "R")


if __name__ == "__main__":
    main()
