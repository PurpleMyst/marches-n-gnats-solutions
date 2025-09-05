from utils import SAME, Program

# On the input tape, you'll get a Roman numeral (1-3999). Your task is to convert it to a unary
# number. For example, if the input tape is `IX`, your output tape should be `|||||||||`.

NUMERALS = [
    ("I", 1),
    ("V", 5),
    ("X", 10),
    ("L", 50),
    ("C", 100),
    ("D", 500),
    ("M", 1000),
]
NUMERAL_SYMBOLS = {sym for sym, _ in NUMERALS}

CAN_SUBTRACT = {
    "I": {"V", "X"},
    "X": {"L", "C"},
    "C": {"D", "M"},
}

CAN_ADD = {}
for sym, value in NUMERALS:
    if 2 * value < 1000:
        CAN_ADD[value] = {sym}
    if 3 * value < 1000:
        CAN_ADD[2 * value] = {sym}


def main() -> None:
    with Program() as p:
        seen_values = set()

        for sym, value in NUMERALS:
            p("INIT", sym, f"SAW_{value}", "_", "R")
            seen_values.add(value)

            for larger_sym, larger_value in NUMERALS:
                if larger_sym not in CAN_SUBTRACT.get(sym, set()):
                    continue
                p(f"SAW_{value}", larger_sym, f"ADD_{larger_value - value}", "_", "R")
                seen_values.add(larger_value - value)

        for value, syms in CAN_ADD.items():
            for sym in NUMERAL_SYMBOLS:
                if sym in syms:
                    add_value = dict(NUMERALS)[sym]
                    p(f"SAW_{value}", sym, f"SAW_{value + add_value}", "_", "R")
                    seen_values.add(value + add_value)
                elif sym not in CAN_SUBTRACT.get({v: k for k, v in NUMERALS}.get(value, ""), set()):
                    p(f"SAW_{value}", sym, f"ADD_{value}", SAME, "R")

        for value in seen_values:
            p.find(
                f"ADD_{value}",
                "_",
                {"|", *NUMERAL_SYMBOLS},
                "R",
                f"ADD_{value - 1}" if value != 1 else "NEXT",
                "|",
                "R" if value != 1 else "L",
            )

            p.find(
                f"SAW_{value}",
                "_",
                "|",
                "R",
                f"ADD_{value - 1}" if value != 1 else "HALT",
                "|",
                "R",
            )

            if value not in CAN_ADD:
                p.ignore(f"SAW_{value}", NUMERAL_SYMBOLS, "R")

        for value in range(1, max(seen_values)):
            if value in seen_values:
                continue
            p(f"ADD_{value}", "_", f"ADD_{value - 1}" if value != 1 else "NEXT", "|", "R")

        p.find("NEXT", "_", {*NUMERAL_SYMBOLS, "|"}, "L", "INIT", "_", "R")
        p("INIT", "|", "HALT", "|", "L")


if __name__ == "__main__":
    main()
