from utils import SAME, Program

DIV = "÷"

MARK_LHS = "L"
MARK_RHS = "R"


def main() -> None:
    with Program() as p:
        p("INIT", "|", "ADD_COMMA", SAME, "L")
        p("ADD_COMMA", "_", "FIND_DIV", ",", "R")

        p.find("FIND_DIV", DIV, {"|", ",", MARK_LHS}, "R", "NEXT_RHS", SAME, "R")

        p.find("NEXT_RHS", "|", MARK_RHS, "R", "NEXT_LHS", MARK_RHS, "L")
        p.find("NEXT_LHS", "|", {MARK_RHS, MARK_LHS, DIV}, "L", "FIND_DIV", MARK_LHS, "R")

        p("NEXT_RHS", "_", "UNMARK_RHS", SAME, "L")
        p("UNMARK_RHS", MARK_RHS, SAME, "_", "L")
        p("UNMARK_RHS", DIV, "UNMARK_LHS", "|", "L")
        p("UNMARK_LHS", MARK_LHS, SAME, "|", "L")
        p("UNMARK_LHS", "|", "ADD_DIV", SAME, "R")
        p("UNMARK_LHS", ",", "EARLY_FINISH", SAME, "R")
        p("ADD_DIV", "|", "FIND_COMMA", DIV, "L")
        p.find("FIND_COMMA", ",", "|", "L", "INC_QUOT", SAME, "L")
        p.find("INC_QUOT", "_", "|", "L", "FIND_DIV", "|", "R")
        p("NEXT_LHS", ",", "CLEAN", ",", "R")
        p("CLEAN", MARK_LHS, SAME, "|", "R")
        p("CLEAN", {DIV, MARK_RHS, "|"}, SAME, "_", "R")
        p("CLEAN", "_", "HALT", "_", "L")
        p("EARLY_FINISH", "|", "EARLY_FINISH", "_", "R")
        p("EARLY_FINISH", "_", "LAST_INC_QUOT", "_", "L")
        p.find("LAST_INC_QUOT", ",", "_", "L", "READD_COMMA", "|", "R")
        p("READD_COMMA", "_", "HALT", ",", "R")


if __name__ == "__main__":
    main()
