from utils import SAME, Program

DIV = "÷"

LHS = "l"
RHS = "r"

POPPED_LHS = "L"


def main() -> None:
    with Program() as p:
        p("INIT", "|", "CONV_LHS", "|", "R")
        p("CONV_LHS", "|", SAME, LHS, "R")
        p("CONV_LHS", DIV, "CONV_RHS", LHS, "R")
        p("CONV_RHS", "|", SAME, RHS, "R")
        p("CONV_RHS", "_", "POP_RHS_OR_INC_QUOT", SAME, "L")
        p("CONV_RHS", POPPED_LHS, SAME, SAME, "R")

        p("POP_RHS_OR_INC_QUOT", RHS, "POP_LHS", "_", "L")
        p("POP_RHS_OR_INC_QUOT", POPPED_LHS, "POP_RHS_OR_INC_QUOT", "|", "L")

        p("POP_LHS", POPPED_LHS, SAME, SAME, "L")
        p("POP_LHS", RHS, SAME, "|", "L")
        p("POP_LHS", LHS, "CONV_RHS", POPPED_LHS, "R")

        p("POP_RHS_OR_INC_QUOT", LHS, SAME, SAME, "L")
        p("POP_RHS_OR_INC_QUOT", POPPED_LHS, SAME, "|", "L")
        p("POP_RHS_OR_INC_QUOT", "|", SAME, "/", "L")
        p("POP_RHS_OR_INC_QUOT", "_", "CONV_RHS", "|", "R")

        p("CONV_RHS", "/", SAME, "|", "R")
        p("CONV_RHS", LHS, SAME, SAME, "R")

        p("POP_LHS", "|", "CLEAN", ",", "R")
        p("CLEAN", POPPED_LHS, SAME, "|", "R")
        p("CLEAN", "|", SAME, "_", "R")
        p("CLEAN", "_", "HALT", SAME, "L")


if __name__ == "__main__":
    main()
