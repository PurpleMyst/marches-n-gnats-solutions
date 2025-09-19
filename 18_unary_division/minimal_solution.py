from utils import SAME, Program

DIV = "÷"

MARK_LHS = "L"


def main() -> None:
    with Program() as p:
        p("INIT", "|", "ADD_COMMA", SAME, "L")
        p("ADD_COMMA", "_", "FIND_EOT", ",", "R")

        p.find("FIND_EOT", "_", {"|", ",", DIV, MARK_LHS}, "R", "NEXT_RHS", SAME, "L")

        p("NEXT_RHS", "|", "NEXT_DIV_LHS", "_", "L")
        p("NEXT_RHS", DIV, "UNMARK_LHS", "|", "L")
        p.find("NEXT_LHS", "|", MARK_LHS, "L", "FIND_EOT", MARK_LHS, "R")
        p.find("NEXT_DIV_LHS",DIV, "|", "L", "NEXT_LHS", SAME, "L")

        p("UNMARK_LHS", MARK_LHS, SAME, "|", "L")
        p("UNMARK_LHS", "|", "ADD_DIV", SAME, "R")
        p("UNMARK_LHS", ",", "EARLY_FINISH", "|", "R")
        p("ADD_DIV", "|", "INC_QUOT", DIV, "L")
        p.find("INC_QUOT", "_", {"|", ","}, "L", "FIND_EOT", "|", "R")
        p("NEXT_LHS", ",", "CLEAN", ",", "R")
        p("CLEAN", MARK_LHS, SAME, "|", "R")
        p("CLEAN", {DIV, "|"}, SAME, "_", "R")
        p("CLEAN", "_", "HALT", "_", "L")
        p("EARLY_FINISH", "|", "CLEAN", ",", "R")


if __name__ == "__main__":
    main()
