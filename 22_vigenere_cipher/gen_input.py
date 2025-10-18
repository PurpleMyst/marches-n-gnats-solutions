from pathlib import Path

PANGRAMS = [
    "The quick brown fox jumps over the lazy dog.",
    "Pack my box with five dozen liquor jugs.",
    "How vexingly quick daft zebras jump!",
    "Sphinx of black quartz, judge my vow.",
    "The five boxing wizards jump quickly.",
    "Jackdaws love my big sphinx of quartz.",
    "Waltz, bad nymph, for quick jigs vex.",
    "Jived fox nymph grabs quick waltz.",
    "Bright vixens jump; dozy fowl quack.",
    "Quick zephyrs blow, vexing daft Jim.",
]

KEYS = {"j", "jj", "jjj", "jjjj", "jjjjj"}
for p in PANGRAMS:
    for w in p.split():
        w = "".join(c.lower() for c in w if c.isalpha())
        KEYS.add(w)


def vigenere(plaintext, key):
    from itertools import cycle

    ciphertext = []
    for p_char, k_char in zip(plaintext, cycle(key)):
        p_val = ord(p_char) - ord("a")
        k_val = ord(k_char) - ord("a")
        c_val = (p_val + k_val) % 26
        c_char = chr(c_val + ord("a"))
        ciphertext.append(c_char)
    return "".join(ciphertext)


def main() -> None:
    with open(Path(__file__).parent / "input.txt", "w", newline="\n") as f:
        for p in PANGRAMS:
            p = "".join(c.lower() for c in p if c.isalpha())
            for k in KEYS:
                ciphertext = vigenere(p, k)
                print(p, k, ciphertext)
                tape = f"{k}:{ciphertext}"
                f.write(f"{tape} => {p}\n")


if __name__ == "__main__":
    main()
