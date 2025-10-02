# pyright: strict
from string import ascii_lowercase, ascii_uppercase

from utils import SAME, Program

DIGITS = frozenset(range(1, 10))
TAPE_SYMBOLS = {*map(str, DIGITS), *ascii_lowercase[: max(DIGITS)], "o", "0", "=", "|", "!", "/", "\\", "@", "$"}
SEEN_MARKERS = set(ascii_uppercase[: max(DIGITS)])


def mark(d: int | str) -> str:
    if d in DIGITS:
        return ascii_lowercase[d - 1]
    elif d == "0":
        return "o"
    elif d == "=":
        return "!"
    elif d == "|":
        return "/"
    elif d == "/":
        return "\\"
    else:
        raise ValueError(f"Invalid marked character: {d}")


MARKED_DIGITS = {mark(d) for d in DIGITS} | {mark("0")}


def seen(d: int) -> str:
    assert d in DIGITS
    return ascii_uppercase[d - 1]


def main() -> None:
    with Program() as p:
        # Remove all leftover symbols from the tape.
        p("CLEAN", {*TAPE_SYMBOLS, *SEEN_MARKERS, "@"}, "CLEAN", "_", "R")
        p("CLEAN", "_", "HALT", SAME, "R")

        # Go to the start of the tape, mark the found conflict and then clean the tape.
        p.find("PRE_CLEAN", "_", SEEN_MARKERS, "L", "CLEAN", "N", "R")

        # Clean up moving left (happens when the grid is valid).
        p("LEFTWARDS_CLEAN", {*TAPE_SYMBOLS, *SEEN_MARKERS, "@"}, "LEFTWARDS_CLEAN", "_", "L")
        p("LEFTWARDS_CLEAN", "_", "HALT", SAME, "R")

        # Move on to the net row/column/box.
        p.find("ROW_RESTART", "_", {*TAPE_SYMBOLS, *SEEN_MARKERS, "@"}, "L", "PRE_ROW", "_", "R")
        p.find(
            "COL_RESTART",
            "_",
            {*TAPE_SYMBOLS, *SEEN_MARKERS, "@"} - {mark("=")},
            "L",
            "PRE_COL",
            "_",
            "R",
        )
        p.find(
            "BOX_RESTART",
            "_",
            {*TAPE_SYMBOLS, *SEEN_MARKERS, "@"} - {mark("|")},
            "L",
            "PRE_BOX",
            "_",
            "R",
        )
        p("COL_RESTART", mark("="), SAME, "=", "L")
        p("BOX_RESTART", mark("|"), SAME, mark(mark("|")), "L")

        # Skip over the seen markers and move into the row/col/box state.
        for s in ("ROW", "COL", "BOX"):
            p(f"PRE_{s}", SEEN_MARKERS, SAME, "_", "R")
            p(f"PRE_{s}", "@", s, SAME, "R")
        p.ignore("PRE_COL", "_", "R")

        # Mark the start of the tape.
        p("MARK_SOT", "_", "ROW", "@", "R")
        p("INIT", "0", "MARK_SOT", SAME, "L")

        for d in DIGITS:
            p("INIT", str(d), "MARK_SOT", SAME, "L")

            # When we see a digit, add it to the seen markers.
            p("ROW", str(d), f"ROW_ADD_{d}", mark(d), "L")
            p("COL", str(d), f"COL_ADD_{d}", mark(d), "L")
            p("BOX", str(d), f"BOX_ADD_{d}", mark(d), "L")
            p.find(
                f"ROW_ADD_{d}",
                "_",
                {*TAPE_SYMBOLS, *SEEN_MARKERS, "@"} - {seen(d)},
                "L",
                "ROW",
                seen(d),
                "R",
            )
            p.find(
                f"COL_ADD_{d}",
                "_",
                {*TAPE_SYMBOLS, *SEEN_MARKERS, "@"} - {seen(d)},
                "L",
                "COL_NL",
                seen(d),
                "R",
            )
            p.find(
                f"BOX_ADD_{d}",
                "_",
                {*TAPE_SYMBOLS, *SEEN_MARKERS, "@", mark(mark("|"))} - {seen(d)},
                "L",
                "BOX",
                seen(d),
                "R",
            )

            # If we see the marker for the digit we're trying to add, we have a conflict.
            p(f"ROW_ADD_{d}", seen(d), "PRE_CLEAN", SAME, "L")
            p(f"COL_ADD_{d}", seen(d), "PRE_CLEAN", SAME, "L")
            p(f"BOX_ADD_{d}", seen(d), "PRE_CLEAN", SAME, "L")

            # Stuff we can ignore.
            p.ignore("ROW", {mark(d), "|", "0", mark("="), *SEEN_MARKERS, "@"}, "R")
            p.ignore("COL", {*MARKED_DIGITS, "|"}, "R")
            p.ignore("BOX", {mark(d), "=", "0", *SEEN_MARKERS, "@", mark(mark("|"))}, "R")

            # End of box: move to the next row.
            p("BOX", {"|", mark("|")}, "BOX_NL", mark("|"), "R")

            # End of three-row set: move to next one.
            p("BOX", "$", "BOX_RESTART", "=", "L")

            # Go to the next row.
            p.find(
                "COL_NL",
                "=",
                {*TAPE_SYMBOLS, *SEEN_MARKERS, "@"} - {"="},
                "R",
                "COL",
                mark("="),
                "R",
            )
            p.find(
                "BOX_NL",
                "=",
                {*TAPE_SYMBOLS, *SEEN_MARKERS, "@"} - {"$", "="},
                "R",
                "BOX",
                SAME,
                "R",
            )

            # End of current box: move to the next one.
            p("BOX_NL", {"$", "_"}, "BOX_RESTART", SAME, "L")

            # Reaching the end of the tape in the BOX state means we are done.
            p("BOX", "_", "LEFTWARDS_CLEAN", "Y", "L")

            # We can directly skip to the next column when we see a zero, nothing to add.
            p("COL", "0", "COL_NL", mark("0"), "R")

            # End of column: move to the next one.
            p("COL_NL", "_", "COL_RESTART", SAME, "L")

            # End of row: move to the next one.
            p("ROW", "=", "ROW_RESTART", mark("="), "L")

            # End of row checking: move on to column checking.
            p("ROW", "_", "ROW_DONE", SAME, "L")
            p("ROW_DONE", mark(d), SAME, str(d), "L")
            p.ignore("ROW_DONE", {"|", "0", "@"}, "L")
            p("ROW_DONE", mark("="), SAME, "=", "L")
            p("ROW_DONE", SEEN_MARKERS, SAME, "_", "L")
            p("ROW_DONE", "_", "PRE_COL", SAME, "R")

            # End of column checking: move on to box checking.
            p("COL", "=", "COL_DONE", SAME, "R")
            p.find(
                "COL_DONE",
                "_",
                {*TAPE_SYMBOLS, *SEEN_MARKERS, "@"},
                "L",
                "PREPARE_FOR_BOX",
                "_",
                "R",
            )

            # Prepare for box checking: move back to the start of the tape, unmarking stuff.
            # We also mark the end of every three-row set.
            p({"PREPARE_FOR_BOX", "PREPARE_FOR_BOX_1", "PREPARE_FOR_BOX_2"}, mark(d), SAME, str(d), "R")
            p({"PREPARE_FOR_BOX", "PREPARE_FOR_BOX_1", "PREPARE_FOR_BOX_2"}, SEEN_MARKERS, SAME, "_", "R")
            p({"PREPARE_FOR_BOX", "PREPARE_FOR_BOX_1", "PREPARE_FOR_BOX_2"}, mark("0"), SAME, "0", "R")
            p("PREPARE_FOR_BOX", {mark("="), "="}, "PREPARE_FOR_BOX_1", "=", "R")
            p("PREPARE_FOR_BOX_1", {mark("="), "="}, "PREPARE_FOR_BOX_2", "=", "R")
            p("PREPARE_FOR_BOX_2", {mark("="), "="}, "PREPARE_FOR_BOX", "$", "R")
            p.ignore({"PREPARE_FOR_BOX", "PREPARE_FOR_BOX_1", "PREPARE_FOR_BOX_2"}, {"@", "|"}, "R")
            p({"PREPARE_FOR_BOX", "PREPARE_FOR_BOX_1", "PREPARE_FOR_BOX_2"}, "_", "RETURN_FOR_BOX", SAME, "L")
            p.find("RETURN_FOR_BOX", "@", {*TAPE_SYMBOLS, *SEEN_MARKERS, "$"} - {"@"}, "L", "BOX", SAME, "R")


if __name__ == "__main__":
    main()
