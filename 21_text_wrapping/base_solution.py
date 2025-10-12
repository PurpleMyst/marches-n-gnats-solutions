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
        p.ignore("INIT", {"|", "/", ":", *UP_LETTERS, "=", "+"}, "R")

        for l in LETTERS:
            p("INIT", l, "MARK", l.upper(), "L")
        p("INIT", "-", "MARK", "=", "L")
        p("INIT", "_", "CLEAN", "_", "L")

        p.find("MARK", "|", {*LETTERS, *UP_LETTERS, ":", "/", "=", "+"}, "L", "INIT", "/", "R")
        p("MARK", "_", "NL", "_", "R")

        p("NL", "/", SAME, "|", "R")
        for l in LETTERS:
            p("NL", l, SAME, l.upper(), "R")
        p.ignore("NL", {*UP_LETTERS, "=", ":", "+"}, "R")
        p("NL", {"-", "_"}, "READY", SAME, "L")
        for l in LETTERS:
            p("READY", l.upper(), SAME, l, "L")
        p("READY", "=", "INIT", "+", "R")

        for l in LETTERS:
            p("CLEAN", l.upper(), SAME, l, "L")
        p("CLEAN", "/", SAME, "_", "L")
        p("CLEAN", "|", SAME, "_", "L")
        p("CLEAN", ":", SAME, "_", "L")
        p("CLEAN", "=", SAME, "-", "L")
        p("CLEAN", "+", SAME, "+", "L")
        p("CLEAN", "_", "HALT", "_", "R")

if __name__ == "__main__":
    main()
