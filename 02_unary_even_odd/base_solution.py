from utils import Program


def main() -> None:
    with Program() as p:
        p("INIT", "|", "ODD", "_", "R")
        p("ODD", "|", "INIT", "_", "R")
        p("INIT", "_", "HALT", "E", "R")
        p("ODD", "_", "HALT", "O", "R")


if __name__ == "__main__":
    main()
