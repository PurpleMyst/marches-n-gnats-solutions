from utils import SAME, Program

LETTERS = set("abcdefghijklmnopqrstuvwxyz")
UP_LETTERS = {l.upper() for l in LETTERS}

# On the input tape, you'll get the line wrapping length as a unary number and the text (separated
# by `:`). Your task is to wrap the text so that each line is at most the given length.
#
# You must use greedy left-to-right wrapping (i.e., keep appending the next word if it still fits on
# the line). Mark line breaks using `+`. The words are never broken; line breaks can only occur
# between words.
#
# Each line consists of English letters (`a-z`), `-` is used as a word delimiter. There are no
# consecutive hyphens and no leading/trailing hyphens. The line length includes the in-line hyphens
# (`-`) but not line breaks (`+`).
#
# The wrapping length is at least as long as the longest word in the text, but no longer than the
# whole text.
#
# ### Examples
# - If the input tape is `|||||||:hello-world-how-are-you`, your output tape should be
# `hello+world+how-are+you` (each line is max 7 characters).
# - If the input tape is `|||||:hello-world-how-are-you`, your output tape should be
# `hello+world+how+are+you` (each line is max 5 characters).
# - If the input tape is `|||||||:hey-you`, your output tape should be `hey-you` (whole text fits into
# 1 line of 7 characters).


def main() -> None:
    with Program() as p:
        p("INIT", "|", "PROC", "_", "R")

        p("PROC", ":", SAME, "|", "R")
        p.ignore("PROC", {"|", "/", *UP_LETTERS, "=", "+"}, "R")

        for l in LETTERS:
            p("PROC", l, "MARK", l.upper(), "L")
        p("PROC", "-", "MARK", "=", "L")
        p("PROC", "_", "CLEAN", "_", "L")

        p.find("MARK", "|", {*UP_LETTERS, "/", "=", "+"}, "L", "PROC", "/", "R")
        p("MARK", "_", "NL", "_", "R")

        p("NL", "/", SAME, "|", "R")
        p.ignore("NL", {*UP_LETTERS, "=", "+"}, "R")
        p("NL", {*LETTERS, "-", "_"}, "READY", SAME, "L")
        for l in LETTERS:
            p("READY", l.upper(), SAME, l, "L")
        p("READY", "=", "PROC", "+", "R")

        for l in LETTERS:
            p("CLEAN", l.upper(), SAME, l, "L")
        p("CLEAN", "/", SAME, "_", "L")
        p("CLEAN", "|", SAME, "_", "L")
        p("CLEAN", "=", SAME, "-", "L")
        p("CLEAN", "+", SAME, "+", "L")
        p("CLEAN", "_", "HALT", "_", "R")


if __name__ == "__main__":
    main()
