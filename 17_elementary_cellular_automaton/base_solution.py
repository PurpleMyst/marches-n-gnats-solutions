from utils import SAME, Program

ALIVE = "+"
DEAD = "-"

NUMBERS = set("12345")


def main() -> None:
    with Program() as p:
        # At the start, mark number of generations left (after the initial one), then move on to
        # evolving.
        p("INIT", ALIVE, "MARK", SAME, "L")
        p("INIT", DEAD, "HALT", "_", "L")
        p("MARK", "_", "SKIP_FIRST", "5", "R")

        # EVOLVE_PAST_DEAD: means we are moving right and came from a dead cell.

        ## We see another dead cell: this can't affect the previous cell and the current one must
        ## stay dead so far, so just move right.
        p("EVOLVE_PAST_DEAD", DEAD, "EVOLVE_PAST_DEAD", SAME, "R")

        ## We see an alive cell: we must go back because the previous cell could be affected.
        p("EVOLVE_PAST_DEAD", ALIVE, "EVOLVE_PAST_DEAD_SAW_ALIVE", SAME, "L")

        ## If we find the previous cell still dead, we can revive it.
        p("EVOLVE_PAST_DEAD_SAW_ALIVE", DEAD, "SKIP_PROCESSED", ALIVE, "R")

        ## If the previous cell was dead and now it's alive, it means it was revived by the cell to
        ## its left, so it must be killed.
        p("EVOLVE_PAST_DEAD_SAW_ALIVE", ALIVE, "SKIP_PROCESSED", DEAD, "R")

        ## Having changed the previous cell, we can move on.
        p("SKIP_PROCESSED", ALIVE, "EVOLVE_PAST_ALIVE", SAME, "R")

        # EVOLVE_PAST_DEAD: means we are moving right and came from a live cell.

        ## A dead cell can't affect anything.
        p("EVOLVE_PAST_ALIVE", DEAD, "EVOLVE_PAST_DEAD", ALIVE, "R")
        p("EVOLVE_PAST_ALIVE", ALIVE, "EVOLVE_PAST_ALIVE_SAW_ALIVE", DEAD, "L")

        p("EVOLVE_PAST_ALIVE_SAW_ALIVE", {ALIVE, DEAD}, "SKIP_PROCESSED", DEAD, "R")
        p("SKIP_PROCESSED", DEAD, "EVOLVE_PAST_ALIVE", SAME, "R")

        p("EVOLVE_PAST_ALIVE", "_", "RETURN", "+", "L")

        # RETURN: means we're moving back to the start
        p.ignore("RETURN", {ALIVE, DEAD}, "L")
        for n in NUMBERS:
            is_last = n == "1"
            next_n = str(int(n) - 1)

            p("RETURN", n, f"RESTART_{n}" if not is_last else "HALT", "+", "L")

            if not is_last:
                p(f"RESTART_{n}", "_", "SKIP_FIRST", next_n, "R")
                p("SKIP_FIRST", ALIVE, "EVOLVE_PAST_ALIVE", SAME, "R")


if __name__ == "__main__":
    main()
