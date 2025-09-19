from utils import SAME, Program

DIV = "÷"
DEAD = "."

MARK_LHS = "L"
MARK_RHS = "R"


def main() -> None:
    with Program() as p:
        p.find("INIT", DIV, {"|", MARK_LHS}, "R", "NEXT_RHS", SAME, "R")
        p.find("NEXT_RHS", "|", MARK_RHS, "R", "NEXT_LHS", MARK_RHS, "L")
        p("NEXT_RHS", DEAD, "FIND_QUOT_START", DEAD, "R")
        p.find("NEXT_LHS", "|", {MARK_RHS, MARK_LHS, DIV}, "L", "INIT", MARK_LHS, "R")
        p.find("FIND_QUOT_START", "_", {DEAD}, "R", "INC_QUOT", SAME, "R")
        p("NEXT_RHS", "_", "INC_QUOT", "_", "R")
        p.find("INC_QUOT", "_", "|", "R", "RETURN_QUOT", "|", "L")
        p.find("RETURN_QUOT", "_", "|", "L", "UNMARK_RHS", SAME, "L")
        p("UNMARK_RHS", MARK_RHS, "UNMARK_RHS", DEAD, "L")
        p("UNMARK_LHS", MARK_LHS, "UNMARK_LHS", "|", "L")
        p.ignore("UNMARK_RHS", DEAD, "L")
        p("UNMARK_RHS", DIV, "UNMARK_LHS", "|", "L")
        p("UNMARK_LHS", "|", "ADD_DIV", SAME, "R")
        p("ADD_DIV", "|", "NEXT_RHS", DIV, "R")
        p("UNMARK_LHS", "_", "EARLY_CLEAN", "_", "R")
        p("NEXT_LHS", "_", "PRIME_REM", "_", "R")

        p("PRIME_REM", MARK_LHS, "FIND_REM_SPACE1", "_", "R")
        p.find("FIND_REM_SPACE1", "_", {MARK_LHS, DEAD}, "R", "FIND_REM_SPACE2", SAME, "R")
        p("FIND_REM_SPACE1", {MARK_RHS, DIV, "|"}, SAME, DEAD, "R")
        p.find("FIND_REM_SPACE2", "_", "|", "R", "MARK_FIRST_REM", ",", "R")
        p("MARK_FIRST_REM", "_", "RETURN_REM", "|", "L")
        p.find("RETURN_REM", "_", set("|,"), "L", "NEXT_REM", SAME, "L")
        p.find("NEXT_REM", MARK_LHS, DEAD, "L", "INC_REM1", DEAD, "R")
        p.find("INC_REM1", "_", DEAD, "R", "INC_REM2", SAME, "R")
        p.find("INC_REM2", "_", {"|", ","}, "R", "RETURN_REM", "|", "L")
        p("NEXT_REM", "_", "CLEAN", "_", "R")
        p("CLEAN", DEAD, "CLEAN", "_", "R")
        p("CLEAN", "_", "HALT", "_", "R")

        p("EARLY_CLEAN", {DEAD, "|"}, "EARLY_CLEAN", "_", "R")
        p("EARLY_CLEAN", "_", "ADD_COMMA", "_", "R")
        p.find("ADD_COMMA", "_", "|", "R", "HALT", ",", "R")


if __name__ == "__main__":
    main()
