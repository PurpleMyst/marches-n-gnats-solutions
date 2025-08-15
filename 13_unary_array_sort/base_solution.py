from utils import Program

# On the input tape, you'll get one or more positive numbers in the unary format separated by
# commas. Your task is to sort these numbers in ascending order. For example, if the input tape is
# `||,|,|||||,||||||||`, your output tape should be `|,||,|||||,||||||||`.
# ------------------------------------------------------------------------------------------------
# Bubble-ish sort implementation, i guess.

MAX_ITEM = 375


def main() -> None:
    with Program() as p:
        # Mark the end of the "to be sorted" part of the tape with "H".
        p("INIT", "|", "MARK_END", "|", "R")
        p.find("MARK_END", "_", {"|", ","}, "R", "RETURN", "H", "L")
        p.find("RETURN", "_", {"|", ","}, "L", "DOIT", "_", "R")

        # The "GOBACK" state is responsible for marking the new "to be sorted" part of the tape, by
        # finding the previous comma and marking the end of the tape with "H".
        p.find("GOBACK", ",", "|", "L", "RETURN", "H", "L")
        p("GOBACK", "_", "CLEAN", "_", "R")

        # After we're done sorting, the "CLEAN" state takes care of removing the leftover comma at
        # the end of the tape.
        p.find("CLEAN", "_", {"|", ","}, "R", "LAST", "_", "L")
        p("LAST", ",", "HALT", "_", "R")

        # The "DOIT" state loads the left-hand side of the tape into state LHS_n, then compares it
        # to the following item; if the left-hand side is greater, it swaps the two items by moving
        # to the "SWAP" state, otherwise the "SKIP" state moves on to the next pair of items.
        for n in range(1, MAX_ITEM):
            p(f"LHS_{n}", "H", f"GOBACK", ",", "L")

            # Load left-hand side into state, going to state CMP_n once fully loaded
            p("DOIT" if n == 1 else f"LHS_{n - 1}", "|", f"LHS_{n}", "|", "R")
            p(f"LHS_{n}", ",", f"CMP_{n}", ",", "R")

            # For each unit in the right-hand side, decrement our state; if we get to the comma
            # without having finished, that means our left-hand side was greater and we must swap.
            p(f"CMP_{n}", "|", f"CMP_{n - 1}", "|", "R")
            p(f"CMP_{n}", ",", "SWAP", ",", "L")
            p(f"CMP_{n}", "H", "SWAP", "H", "L")

        # State "CMP_0" means LHS <= RHS, so we can either skip or move on to the next iteration.
        p("CMP_0", ",", "SKIP", ",", "L")
        p("CMP_0", "|", "SKIP", "|", "L")
        p("CMP_0", "H", "GOBACK", ",", "L")

        # State "SKIP" means RHS >= LHS, so we just need to go back to the RHS and continue.
        p.find("SKIP", ",", "|", "L", "DOIT", ",", "R")

        # "SWAP" state
        # ||||||,|||,
        #          ^ We are here at this point
        # We'll fully replace the right-hand side with asterisks, then move on to the "POP_MARK"
        # state.
        p("SWAP", "|", "SWAP", "*", "L")
        p("SWAP", ",", "POP_MARK", ",", "R")

        # "POP_MARK" state
        # ||||||,***,
        #        ^ We are here at this point
        # The states here do:
        # 1) POP_MARK => Remove *, replace with !
        # 2) BACK_TO_RHS_COMMA => Go back to comma of RHS
        # 3) BACK_TO_LHS_COMMA => Go back to comma of LHS
        # 4) PLACE_BANG => Mark the LHS with !
        # 4) BACK_TO_RHS => Go back to RHS
        p.find("POP_MARK", "*", "|", "R", "BACK_TO_RHS_COMMA", "|", "L")
        p.find("BACK_TO_RHS_COMMA", ",", "|", "L", "BACK_TO_LHS_COMMA", ",", "L")
        p.find("BACK_TO_LHS_COMMA", ",", {"!", "|"}, "L", "PLACE_BANG", ",", "R")
        p.find("BACK_TO_LHS_COMMA", "_", {"!", "|"}, "L", "PLACE_BANG", "_", "R")
        p("PLACE_BANG", "|", "BACK_TO_RHS", "!", "R")
        p.ignore("PLACE_BANG", "!", "R")
        p.ignore("BACK_TO_RHS", "|", "R")
        p("BACK_TO_RHS", ",", "POP_MARK", ",", "R")

        p("POP_MARK", ",", "DONE_MARKING", ",", "L")
        p("POP_MARK", "H", "DONE_MARKING", "H", "L")

        # "DONE_MARKING" state
        # !!!|||,|||,
        #          ^  We are here at this point
        p.find("DONE_MARKING", "!", {"|", ","}, "L", "PLACE_NEW_COMMA", "!", "R")
        p("PLACE_NEW_COMMA", "|", "REMOVE_OLD_COMMA", ",", "R")

        # "REMOVE_OLD_COMMA" state
        # !!!,||,|||,
        #     ^  We are here at this point
        p.find("REMOVE_OLD_COMMA", ",", "|", "R", "FIND_BANGS", "|", "L")

        # "FIND_BANGS" state
        # !!!,||||||,
        #       ^  We are here at this point
        p.find("FIND_BANGS", "!", {"|", ","}, "L", "REMOVE_BANGS", "|", "L")

        # "REMOVE_BANGS" state
        # !!!,||||||,
        #   ^  We are here at this point
        p("REMOVE_BANGS", "!", "REMOVE_BANGS", "|", "L")
        p("REMOVE_BANGS", ",", "CONTINUE", ",", "R")
        p("REMOVE_BANGS", "_", "CONTINUE", "_", "R")
        p.find("CONTINUE", ",", "|", "R", "DOIT", ",", "R")


if __name__ == "__main__":
    main()
