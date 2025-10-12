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
    "Quick zephyrs blow, vexing daft Jim."
]


def wrap_text(tape):
    n, text = tape.split(':', 1)
    width = len(n)
    words = text.split('-')
    lines, line = [], words[0]
    for w in words[1:]:
        if len(line) + 1 + len(w) <= width:
            line += '-' + w
        else:
            lines.append(line)
            line = w
    lines.append(line)
    return '+'.join(lines)

def main() -> None:
    with open(Path(__file__).parent / "input.txt", "w", newline="\n") as f:
        for p in PANGRAMS:
            min_length = max(map(len, p.split()))
            max_length = len(p)
            p = p.lower().replace(" ", "-").replace(",", "").replace(";", "").replace("!", "").replace(".", "")
            for l in range(min_length, max_length + 1):
                tape = f"{'|' * l}:{p}"
                f.write(f"{tape} => {wrap_text(tape)}\n")


if __name__ == "__main__":
    main()
