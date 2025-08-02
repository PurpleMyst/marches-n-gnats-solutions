from utils import LETTERS, Program


def main() -> None:
    with Program() as p:
        for letter in LETTERS:
            p("INIT", letter, "RIGHT", "_", "R")
            p("RIGHT", letter, "RIGHT", "_", "R")

        for letter in LETTERS | {"+"}:
            p.ignore("INC", letter, "R")
            p.ignore("RETURN", letter, "L")

        p("RIGHT", "+", "INC", "_", "R")
        p.ignore("INC", "|", "R")
        p.ignore("RETURN", "|", "L")
        p("INC", "_", "RETURN", "|", "L")
        p("RETURN", "_", "RIGHT", "_", "R")
        p("RIGHT", "|", "FINISH", "|", "R")
        p("RIGHT", "_", "HALT", "|", "R")

        p.ignore("FINISH", "|", "R")
        p("FINISH", "_", "HALT", "|", "R")


if __name__ == "__main__":
    main()
