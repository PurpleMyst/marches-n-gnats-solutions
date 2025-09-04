from utils import Program

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

IGNORING = {
    1: {"I"},
    5: {"I"},
    10: {"I", "V", "X"},
    40: {"I", "V", "X"},
    50: {"I", "V", "X"},
    90: {"I", "V", "X"},
    100: {"I", "V", "X", "L", "C"},
    400: {"I", "V", "X", "L", "C"},
    500: {"I", "V", "X", "L", "C"},
    900: {"I", "V", "X", "L", "C"},
    1000: {"I", "V", "X", "L", "C", "D", "M"},
}

CAN_SUBTRACT = {
    "I": {"V", "X"},
    "X": {"L", "C"},
    "C": {"D", "M"},
}


def main() -> None:
    with Program() as p:
        seen_values = set()

        for sym, value in NUMERALS:
            p("INIT", sym, f"ADD_{value}", "_", "R")
            seen_values.add(value)

            for larger_sym, larger_value in NUMERALS:
                if larger_sym not in CAN_SUBTRACT.get(sym, set()):
                    continue
                p(f"ADD_{value}", larger_sym, f"ADD_{larger_value - value}", "_", "R")
                seen_values.add(larger_value - value)

        for value in seen_values:
            p.find(
                f"ADD_{value}",
                "_",
                {"|", *IGNORING.get(value, set())},
                "R",
                f"ADD_{value - 1}" if value != 1 else "NEXT",
                "|",
                "R" if value != 1 else "L",
            )

        for value in range(1, max(seen_values)):
            if value in seen_values:
                continue
            p(f"ADD_{value}", "_", f"ADD_{value - 1}" if value != 1 else "NEXT", "|", "R")

        p.find("NEXT", "_", {*NUMERAL_SYMBOLS, "|"}, "L", "INIT", "_", "R")
        p("INIT", "|", "HALT", "|", "L")


if __name__ == "__main__":
    main()
