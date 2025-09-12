from utils import SAME, Program

ALIVE = "+"
DEAD = "-"

NUMBERS = set("12345")

STAYS_ALIVE = "*"
STAYS_DEAD = "/"

WAS_ALIVE_WILL_FLIP = "Z"
WAS_DEAD_WILL_FLIP = "R"


def main() -> None:
    with Program() as p:
        # At the start, mark number of generations left (after the initial one), then move on to
        # evolving.
        p("INIT", {ALIVE, DEAD}, "MARK", SAME, "L")
        p("MARK", "_", "EVOLVE", "5", "R")

        # We see a plus when evolving, we need to check to the left and right if there's a + and, if
        # so, kill it.
        p("EVOLVE", ALIVE, "CHECK_PLUS_LEFT", STAYS_ALIVE, "L")
        p("CHECK_PLUS_LEFT", {ALIVE, STAYS_ALIVE, WAS_ALIVE_WILL_FLIP}, "KILL_PLUS", SAME, "R")
        p(
            "CHECK_PLUS_LEFT",
            {DEAD, STAYS_DEAD, WAS_DEAD_WILL_FLIP, *NUMBERS},
            "CHECK_PLUS_MIDDLE",
            SAME,
            "R",
        )
        p("CHECK_PLUS_MIDDLE", STAYS_ALIVE, "CHECK_PLUS_RIGHT", SAME, "R")
        p("CHECK_PLUS_RIGHT", {ALIVE, STAYS_ALIVE, WAS_ALIVE_WILL_FLIP}, "KILL_PLUS", SAME, "L")
        p("CHECK_PLUS_RIGHT", {DEAD, STAYS_DEAD, WAS_DEAD_WILL_FLIP, "_"}, "KEEP_PLUS", SAME, "L")
        p("KEEP_PLUS", STAYS_ALIVE, "EVOLVE", SAME, "R")
        p("KILL_PLUS", STAYS_ALIVE, "EVOLVE", WAS_ALIVE_WILL_FLIP, "R")

        p("EVOLVE", DEAD, "CHECK_MINUS_LEFT", STAYS_DEAD, "L")
        p(
            "CHECK_MINUS_LEFT",
            {STAYS_DEAD, WAS_DEAD_WILL_FLIP, *NUMBERS},
            "CHECK_MINUS_CENTER_0",
            SAME,
            "R",
        )
        p("CHECK_MINUS_LEFT", {STAYS_ALIVE, WAS_ALIVE_WILL_FLIP}, "CHECK_MINUS_CENTER_1", SAME, "R")
        p("CHECK_MINUS_CENTER_0", STAYS_DEAD, "CHECK_MINUS_RIGHT_0", SAME, "R")
        p("CHECK_MINUS_CENTER_1", STAYS_DEAD, "CHECK_MINUS_RIGHT_1", SAME, "R")
        p("CHECK_MINUS_RIGHT_0", {ALIVE}, "REVIVE_MINUS", SAME, "L")
        p("CHECK_MINUS_RIGHT_1", {ALIVE}, "KEEP_MINUS", SAME, "L")
        p("CHECK_MINUS_RIGHT_0", {DEAD, "_"}, "KEEP_MINUS", SAME, "L")
        p("CHECK_MINUS_RIGHT_1", {DEAD, "_"}, "REVIVE_MINUS", SAME, "L")
        p("KEEP_MINUS", STAYS_DEAD, "EVOLVE", SAME, "R")
        p("REVIVE_MINUS", STAYS_DEAD, "EVOLVE", WAS_DEAD_WILL_FLIP, "R")

        p("EVOLVE", "_", "LAST", "_", "L")
        p("LAST", {WAS_ALIVE_WILL_FLIP, STAYS_ALIVE}, "ADD_PLUS", SAME, "R")
        p("LAST", {WAS_DEAD_WILL_FLIP, STAYS_DEAD}, "NO_PLUS", SAME, "R")
        p("ADD_PLUS", "_", "NEXT_GEN", ALIVE, "L")
        p("NO_PLUS", "_", "NEXT_GEN", SAME, "L")

        for s in ("NEXT_GEN", "NEXT_GEN_SAW_ALIVE", "NEXT_GEN_SAW_DEAD"):
            p(s, STAYS_ALIVE, "NEXT_GEN_SAW_ALIVE", ALIVE, "L")
            p(s, WAS_DEAD_WILL_FLIP, "NEXT_GEN_SAW_DEAD", ALIVE, "L")
            p(s, STAYS_DEAD, "NEXT_GEN_SAW_DEAD", DEAD, "L")
            p(s, WAS_ALIVE_WILL_FLIP, "NEXT_GEN_SAW_ALIVE", DEAD, "L")

        for n in NUMBERS:
            is_last = n == "1"
            p("NEXT_GEN_SAW_ALIVE", n, f"RESTART_{n}" if not is_last else "START_CLEAN", "+", "L")
            p("NEXT_GEN_SAW_DEAD", n, f"RESTART_{n}" if not is_last else "START_CLEAN", "-", "L")

            if not is_last:
                p(f"RESTART_{n}", "_", "EVOLVE", str(int(n) - 1), "R")

        p("START_CLEAN", "_", "CLEAN", "_", "R")
        p("CLEAN", ALIVE, "HALT", SAME, "R")
        p("CLEAN", DEAD, "CLEAN", "_", "R")
        p("CLEAN", "_", "HALT", "_", "R")


if __name__ == "__main__":
    main()
