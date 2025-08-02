from string import ascii_lowercase

from utils import Program

LETTERS = set(ascii_lowercase) | set("äöõü") | set("-")


def main() -> None:
    with Program() as p:
        for letter in LETTERS:
            p("INIT", letter, f"PRIME_{letter}", "_", "L")
            p(f"PRIME_{letter}", "_", f"SEARCH", letter, "R")
            p.ignore("SEARCH", "_", "R")

            p("SEARCH", "*", "TAKE", "_", "R")
            p("SEARCH", letter, f"TOOK_{letter}", "*", "R")
            p("TAKE", letter, f"TOOK_{letter}", "*", "R")
            p.ignore("TAKE", "*", "R")
            p("TAKE", "_", "HALT", "_", "L")

            for other_letter in LETTERS:
                s = f"{letter}{other_letter}"
                p(f"TOOK_{letter}", other_letter, f"TOOK_{s}", "*", "L")
                p(f"TOOK_{letter}", "_", f"FINISH_{letter}", "_", "L")

                p(f"TOOK_{s}", "*", f"TOOK_{s}", "_", "L")
                p(f"FINISH_{letter}", "*", f"FINISH_{letter}", "_", "L")
                p.ignore(f"FINISH_{letter}", "_", "L")
                p.ignore(f"TOOK_{s}", "_", "L")

                for nonspace in LETTERS:
                    p(f"TOOK_{s}", nonspace, f"DROPPING_{s}", nonspace, "L")
                    p(f"FINISH_{letter}", nonspace, f"FINISH_DROPPING_{letter}", nonspace, "L")
                    p.ignore(f"DROPPING_{s}", nonspace, "L")
                    p.ignore(f"FINISH_DROPPING_{letter}", nonspace, "L")

                p(f"DROPPING_{s}", "_", f"DROPPING_{s[1:]}", s[0], "L")
                p(f"FINISH_DROPPING_{letter}", "_", "HALT", letter, "L")
                p(f"DROPPING_{letter}", "_", "RETURN", letter, "R")

            p.ignore("RETURN", "_", "R")
            p.ignore("RETURN", letter, "R")
            p("RETURN", "*", "TAKE", "_", "R")


if __name__ == "__main__":
    main()
