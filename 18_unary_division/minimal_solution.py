from utils import SAME, Program

DIV = "÷"


def main() -> None:
    with Program() as p:
        p("INIT", "|", "ADD_COMMA", SAME, "L")
        p("ADD_COMMA", "_", "GOTO_DIV", ",", "R")

        p.find("GOTO_DIV", DIV, {"|", ","}, "R", "DEC_LHS", SAME, "L")
        p("GOTO_DIV", "_", "CLEAN_BACKWARDS", "_", "L")
        p("CLEAN_BACKWARDS", "|", SAME, "_", "L")
        p("CLEAN_BACKWARDS", ",", "HALT", SAME, "L")

        p("DEC_LHS", "|", "DEC_RHS", DIV, "R")
        p("DEC_LHS", ",", "CLEAN_LHS", ",", "R")
        p("DEC_RHS", {DIV, "_"}, SAME, SAME, "R")
        p("DEC_LHS", {DIV, "_"}, SAME, SAME, "L")
        p("DEC_RHS", "|", "CONTINUE", "_", "R")
        p("CONTINUE", "|", "DEC_LHS", SAME, "L")
        p("CONTINUE", "_", "INC_QUOT", SAME, "L")
        p("INC_QUOT", "_", SAME, SAME, "L")

        p("INC_QUOT", DIV, SAME, "|", "L")
        p("INC_QUOT", "|", "INC_QUOT1", "|", "R")
        p("INC_QUOT", ",", "INC_QUOT2", ",", "L")
        p("INC_QUOT1", "|", "INC_QUOT2", DIV, "L")
        p.find("INC_QUOT2", "_", {"|", ","}, "L", "GOTO_DIV", "|", "R")

        p("CLEAN_LHS", "_", "CLEAN_RHS0", "_", "L")
        p("CLEAN_LHS", DIV, SAME, "|", "R")
        p("CLEAN_LHS", "|", "CLEAN_RHS2", "|", "L")
        p("CLEAN_RHS0", "|", "CLEAN_RHS", "_", "R")
        p("CLEAN_RHS", "|", "CLEAN_RHS2", "_", "R")
        p("CLEAN_RHS2", "|", "CLEAN_RHS2", "_", "R")
        p("CLEAN_RHS2", "_", "HALT", "_", "R")
        p("CLEAN_RHS", "_", SAME, "_", "R")


if __name__ == "__main__":
    main()
