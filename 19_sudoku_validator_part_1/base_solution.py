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
        # Remove
        p("CLEAN", {*TAPE_SYMBOLS, *SEEN_MARKERS, "@"}, "CLEAN", "_", "R")
        p("CLEAN", "_", "HALT", SAME, "R")
        p.find("PRE_CLEAN", "_", SEEN_MARKERS, "L", "CLEAN", "N", "R")
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

        p("LEFTWARDS_CLEAN", {*TAPE_SYMBOLS, *SEEN_MARKERS, "@"}, "LEFTWARDS_CLEAN", "_", "L")
        p("LEFTWARDS_CLEAN", "_", "HALT", SAME, "R")

        for s in ("ROW", "COL", "BOX"):
            p(f"PRE_{s}", SEEN_MARKERS, SAME, "_", "R")
            p(f"PRE_{s}", "@", s, SAME, "R")

        p("MARK_SOT", "_", "ROW", "@", "R")
        p("INIT", "0", "MARK_SOT", SAME, "L")
        for d in DIGITS:
            p("INIT", str(d), "MARK_SOT", SAME, "L")
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

            p(f"ROW_ADD_{d}", seen(d), "PRE_CLEAN", SAME, "L")
            p(f"COL_ADD_{d}", seen(d), "PRE_CLEAN", SAME, "L")
            p(f"BOX_ADD_{d}", seen(d), "PRE_CLEAN", SAME, "L")
            p.ignore("ROW", {mark(d), "|", "0", mark("="), *SEEN_MARKERS, "@"}, "R")
            p.ignore("BOX", {mark(d), "=", "0", *SEEN_MARKERS, "@", mark(mark("|"))}, "R")
            p("BOX", {"|", mark("|")}, "BOX_NL", mark("|"), "R")
            p("BOX", "$", "BOX_RESTART", "=", "L")
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
            p("BOX_NL", {"$", "_"}, "BOX_RESTART", SAME, "L")
            p("BOX", "_", "LEFTWARDS_CLEAN", "Y", "L")
            p("COL", "0", "COL_NL", mark("0"), "R")
            p("COL_NL", "_", "COL_RESTART", SAME, "L")
            p.ignore("COL", {*MARKED_DIGITS, "|"}, "R")

            p("ROW", "=", "ROW_RESTART", mark("="), "L")
            p("ROW", "_", "ROW_DONE", SAME, "L")
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

            p("ROW_DONE", mark(d), SAME, str(d), "L")
            p({"PREPARE_FOR_BOX", "PREPARE_FOR_BOX_1", "PREPARE_FOR_BOX_2"}, mark(d), SAME, str(d), "R")

        p({"PREPARE_FOR_BOX", "PREPARE_FOR_BOX_1", "PREPARE_FOR_BOX_2"}, SEEN_MARKERS, SAME, "_", "R")
        p({"PREPARE_FOR_BOX", "PREPARE_FOR_BOX_1", "PREPARE_FOR_BOX_2"}, mark("0"), SAME, "0", "R")
        p("PREPARE_FOR_BOX", {mark("="), "="}, "PREPARE_FOR_BOX_1", "=", "R")
        p("PREPARE_FOR_BOX_1", {mark("="), "="}, "PREPARE_FOR_BOX_2", "=", "R")
        p("PREPARE_FOR_BOX_2", {mark("="), "="}, "PREPARE_FOR_BOX", "$", "R")
        p.ignore({"PREPARE_FOR_BOX", "PREPARE_FOR_BOX_1", "PREPARE_FOR_BOX_2"}, {"@", "|"}, "R")
        p({"PREPARE_FOR_BOX", "PREPARE_FOR_BOX_1", "PREPARE_FOR_BOX_2"}, "_", "RETURN_FOR_BOX", SAME, "L")
        p.find("RETURN_FOR_BOX", "@", {*TAPE_SYMBOLS, *SEEN_MARKERS, "$"} - {"@"}, "L", "BOX", SAME, "R")


        p.ignore("ROW_DONE", {"|", "0", "@"}, "L")
        p("ROW_DONE", mark("="), SAME, "=", "L")
        p("ROW_DONE", SEEN_MARKERS, SAME, "_", "L")
        p("ROW_DONE", "_", "PRE_COL", SAME, "R")
        p.ignore("PRE_COL", "_", "R")


if __name__ == "__main__":
    main()
