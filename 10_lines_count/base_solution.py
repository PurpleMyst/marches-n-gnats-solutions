from utils import LETTERS, Program

LETTERS &= set("-abdefghijklmnoprstuwyäõöü")


def main() -> None:
    with Program() as p:
        for letter in LETTERS:
            p("INIT", letter, "INIT", "*", "R")
        p.ignore("INIT", "+", "R")

        p("INIT", "_", "COUNT", "|", "L")

        p.ignore("COUNT", "*", "L")
        p.ignore("COUNT", "|", "L")
        p("COUNT", "+", "INCREMENT", "*", "R")
        p.ignore("INCREMENT", "*", "R")

        p.ignore("INCREMENT", "|", "R")
        p("INCREMENT", "_", "COUNT", "|", "L")
        p("COUNT", "_", "CLEAN", "_", "R")
        p("CLEAN", "*", "CLEAN", "_", "R")
        p("CLEAN", "|", "HALT", "|", "R")


if __name__ == "__main__":
    main()
