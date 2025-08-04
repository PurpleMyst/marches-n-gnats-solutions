from utils import Program


def main() -> None:
    with Program() as p:
        p("INIT", "|", "FIND", "_", "R")
        p.ignore("FIND", "|", "R")
        p("FIND", "+", "HALT", "|", "R")


if __name__ == "__main__":
    main()
