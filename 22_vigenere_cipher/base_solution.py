from string import punctuation

from utils import SAME, Program

# On the input tape, you'll get a key and an encrypted message separated by `:`.
# Your task is to decrypt the message using [the Vigenere cipher](https://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher).
# The cipher works as follows:    each letter of the plaintext is shifted forward
# in the alphabet by the position of the corresponding key letter (`a = 0, b = 1, ..., z = 25`).    For example,
# `b (1) + e (4) = f (5)`.    If the shift goes past 25 (`z`), you just subtract 26.    For example, `v (21) + n (13) = i (21 + 13 = 34 - 26 = 8`).
# To decrypt, you shift backward instead.
# The key, the encrypted text, and the plaintext consist only of lowercase Latin
# letters (`a-z`), no spaces or punctuation.    The key is always at least as long as
# the encrypted text (so it never repeats).
# For example, if the input tape is `mdzgstf:thkrg` (`mdzgstf` is the key, `thkrg` is the encrypted message)
# the output tape should be `hello`:
# ```19 (t) - 12 (m) =             7 (h) 7 (h) -  3 (d) =             4 (e)10 (k) -
# 25 (z) = -15 + 26 = 11 (l)17 (r) -  6 (g) =            11 (l) 6 (g) - 18 (s) = -12
# + 26 = 14 (o)```

LETTERS = set("abcdefghijklmnopqrstuvwxyz")
USED_LETTERS = {l: l.upper() for l in LETTERS}

_cs = "".join(c for c in punctuation if c not in {":", "_"})

CIPHER_LETTERS = {l: _cs[ord(l) - ord("a")] for l in LETTERS}
REVERSE_CIPHER_LETTERS = {v: k for k, v in CIPHER_LETTERS.items()}


def main() -> None:
    with Program() as p:
        p.ignore("INIT", LETTERS, "R")
        p("INIT", ":", "MARK", SAME, "R")
        for l in LETTERS:
            p("MARK", l, SAME, CIPHER_LETTERS[l], "R")
        p("MARK", "_", "CR", "_", "L")
        p.find(
            "CR",
            "_",
            {*LETTERS, *CIPHER_LETTERS.values(), *USED_LETTERS.values(), ":"},
            "L",
            "NEXT_KEY",
            SAME,
            "R",
        )
        p.ignore("NEXT_KEY", set(USED_LETTERS.values()), "R")
        p("NEXT_KEY", ":", "RESTART", SAME, "L")

        for l in USED_LETTERS.values():
            p("RESTART", l, "RESTART", l.lower(), "L")
        p("RESTART", "_", "NEXT_KEY", SAME, "R")

        for l in LETTERS:
            p("NEXT_KEY", l, decrypt := f"DECRYPT_{l}", USED_LETTERS[l], "R")
            p.ignore(decrypt, {*LETTERS, ":"}, "R")

            for m in CIPHER_LETTERS.values():
                original_m = REVERSE_CIPHER_LETTERS[m]
                new_m = (ord(original_m) - ord(l)) % 26
                new_m_char = chr(new_m + ord("a"))
                p(decrypt, m, "CR", new_m_char, "L")

            p(decrypt, "_", "DONE", SAME, "L")

        p.ignore("DONE", LETTERS, "L")
        p("DONE", ":", "CLEAN", "_", "L")
        p("CLEAN", {*LETTERS, *USED_LETTERS.values()}, SAME, "_", "L")
        p("CLEAN", "_", "HALT", "_", "R")


if __name__ == "__main__":
    main()
