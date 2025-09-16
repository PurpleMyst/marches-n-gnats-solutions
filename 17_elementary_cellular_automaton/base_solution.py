from utils import SAME, Program

ALIVE = "+"
DEAD = "-"

NUMBERS = set("12345")
LIVE_NUMBERS = set("67890")

STAYS_ALIVE = "*"
STAYS_DEAD = "/"

WAS_ALIVE_WILL_FLIP = "Z"
WAS_DEAD_WILL_FLIP = "R"


def main() -> None:
    with Program() as p:
        # At the start, mark number of generations left (after the initial one), then move on to
        # evolving.
        p("INIT", ALIVE, "MARK", SAME, "L")
        p("INIT", DEAD, "HALT", "_", "L")
        p("MARK", "_", "EVOLVE_PAST_DEAD", "5", "R")

        # EVOLVE_PAST_DEAD: means we are moving right and came from a dead cell.

        ## We see another dead cell: this can't affect the previous cell and the current one must
        ## stay dead so far, so just move right.
        p("EVOLVE_PAST_DEAD", DEAD, "EVOLVE_PAST_DEAD", SAME, "R")

        ## We see an alive cell: we must go back because the previous cell could be affected.
        p("EVOLVE_PAST_DEAD", ALIVE, "EVOLVE_PAST_DEAD_SAW_ALIVE", SAME, "L")

        ## If we find the previous cell still dead, we can revive it.
        p("EVOLVE_PAST_DEAD_SAW_ALIVE", DEAD, "EVOLVE_PAST_REVIVED", ALIVE, "R")

        for n in NUMBERS:
            live_n = str((int(n) + 5) % 10)
            p("EVOLVE_PAST_DEAD_SAW_ALIVE", n, "EVOLVE_PAST_REVIVED", live_n, "R")

        ## If the previous cell was dead and now it's alive, it means it was revived by the cell to
        ## its left, so it must be killed.
        p("EVOLVE_PAST_DEAD_SAW_ALIVE", ALIVE, "EVOLVE_PAST_REVIVED", DEAD, "R")

        ## Having changed the previous cell, we can move on.
        p("EVOLVE_PAST_REVIVED", ALIVE, "EVOLVE_PAST_ALIVE", SAME, "R")

        # EVOLVE_PAST_DEAD: means we are moving right and came from a live cell.

        ## A dead cell can't affect anything.
        p("EVOLVE_PAST_ALIVE", DEAD, "EVOLVE_PAST_DEAD", ALIVE, "R")
        p("EVOLVE_PAST_ALIVE", ALIVE, "EVOLVE_PAST_ALIVE_SAW_ALIVE", DEAD, "L")

        p("EVOLVE_PAST_ALIVE_SAW_ALIVE", {ALIVE, DEAD}, "EVOLVE_PAST_KILLED", DEAD, "R")
        p("EVOLVE_PAST_KILLED", DEAD, "EVOLVE_PAST_ALIVE", SAME, "R")

        p("EVOLVE_PAST_ALIVE", "_", "RETURN", "+", "L")

        # RETURN: means we're moving back to the start
        p.ignore("RETURN", {ALIVE, DEAD}, "L")
        for n in NUMBERS:
            is_last = n == "1"
            next_n = str(int(n) - 1)
            live_n = str((int(n) + 5) % 10)

            p("RETURN", live_n, f"RESTART_{n}" if not is_last else "HALT", "+", "L")

            if not is_last:
                p(f"RESTART_{n}", "_", "EVOLVE_PAST_DEAD", next_n, "R")


if __name__ == "__main__":
    main()
