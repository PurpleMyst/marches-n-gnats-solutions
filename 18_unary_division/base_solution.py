from utils import SAME, Program

DIV = "÷"
DEAD = "."

MARK_LHS = "L"
MARK_RHS = "R"


def main() -> None:
    with Program() as p:
        p.find("INIT", DIV, {"|", MARK_LHS}, "R", "DEC", SAME, "R")
        p.find("DEC", "|", MARK_RHS, "R", "FOUND_DEC", MARK_RHS, "L")
        p("DEC", DEAD, "INC_QUOT0", DEAD, "R")
        p.find("FOUND_DEC", "|", {MARK_RHS, MARK_LHS, DIV}, "L", "INIT", MARK_LHS, "R")
        p.find("INC_QUOT0", "_", {DEAD}, "R", "INC_QUOT", SAME, "R")
        p("DEC", "_", "INC_QUOT", "_", "R")
        p.find("INC_QUOT", "_", "|", "R", "RETURN_QUOT", "|", "L")
        p.find("RETURN_QUOT", "_", "|", "L", "UNMARK", SAME, "L")
        p("UNMARK", MARK_RHS, "UNMARK", DEAD, "L")
        p("UNMARK", MARK_LHS, "UNMARK", "|", "L")
        p.ignore("UNMARK", {DEAD}, "L")
        p("UNMARK", DIV, "UNMARK", "|", "L")
        p("UNMARK", "|", "FAKEOUT", SAME, "R")
        p("FAKEOUT", "|", "DEC", DIV, "R")
        p("UNMARK", "_", "EARLY_CLEAN", "_", "R")
        p("FOUND_DEC", "_", "PRIME_REM", "_", "R")

        p("PRIME_REM", MARK_LHS, "START_REM", "_", "R")
        p.find("START_REM", "_", {MARK_LHS, DEAD, MARK_RHS, DIV, "|"}, "R", "START_REM2", SAME, "R")
        p.find("START_REM2", "_", "|", "R", "START_REM3", ",", "R")
        p("START_REM3", "_", "RETURN_REM", "|", "L")
        p.find("RETURN_REM", "_", set("|,"), "L", "NEXT_REM", SAME, "L")
        p.find("NEXT_REM", MARK_LHS, {MARK_RHS, DEAD, DIV, "|"}, "L", "INC_REM", DEAD, "R")
        p.find("INC_REM", "_", {DEAD, MARK_RHS, DIV, "|"}, "R", "INC_REM2", SAME, "R")
        p.find("INC_REM2", "_", {"|", ","}, "R", "RETURN_REM", "|", "L")
        p("NEXT_REM", "_", "CLEAN", "_", "R")
        p("CLEAN", {DEAD, DIV, MARK_RHS, "|"}, "CLEAN", "_", "R")
        p("CLEAN", "_", "HALT", "_", "R")

        p("EARLY_CLEAN", {DEAD, "|"}, "EARLY_CLEAN", "_", "R")
        p("EARLY_CLEAN", "_", "ADD_COMMA", "_", "R")
        p.find("ADD_COMMA", "_", "|", "R", "HALT", ",", "R")


if __name__ == "__main__":
    main()
