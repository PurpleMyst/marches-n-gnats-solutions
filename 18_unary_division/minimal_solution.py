from utils import SAME, Program

DIV = "÷"


def main() -> None:
    with Program() as p:
        p("INIT", "|", "ADD_COMMA", SAME, "L")
        p("ADD_COMMA", "_", "GOTO_RHS", ",", "R")

        p.find("GOTO_RHS", "_", {"|", ",", DIV}, "R", "NEXT_RHS", SAME, "L")

        p("NEXT_RHS", "|", "GOTO_LHS", "_", "L")
        p("NEXT_RHS", DIV, "INC_QUOT", "|", "L")
        p.find("NEXT_LHS", "|", {DIV}, "L", "GOTO_RHS", DIV, "R")
        p.find("GOTO_LHS", DIV, "|", "L", "NEXT_LHS", SAME, "L")

        p("INC_QUOT", DIV, SAME, "|", "L")
        p("INC_QUOT", "|", "INC_QUOT1", "|", "R")
        p("INC_QUOT", ",", "INC_QUOT1", ",", "R")
        p("INC_QUOT1", "|", "INC_QUOT2", DIV, "L")
        p.find("INC_QUOT2", "_", {"|", ","}, "L", "GOTO_RHS", "|", "R")
        p("NEXT_LHS", ",", "CLEAN_LHS", ",", "R")

        p("CLEAN_LHS", "_", "CLEAN_RHS", "_", "L")
        p("CLEAN_LHS", DIV, SAME, "|", "R")
        p("CLEAN_LHS", "|", "CLEAN_RHS", "|", "L")
        p("CLEAN_RHS", "|", SAME, "_", "R")
        p("CLEAN_RHS", "_", "HALT", "_", "R")


if __name__ == "__main__":
    main()
