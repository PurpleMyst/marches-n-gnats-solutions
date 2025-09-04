from utils import Program

# On the input tape, you'll get a Roman numeral (1-3999). Your task is to convert it to a unary
# number.
# For example, if the input tape is `IX`, your output tape should be `|||||||||`.

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

def main() -> None:
    with Program() as p:
        seen_values = {}

        for (idx, (sym, value)) in enumerate(NUMERALS):
            p("INIT", sym, f"ADD_{value}", "_", "R")
            seen_values.setdefault(value, set())

            for (larger_sym, larger_value) in NUMERALS[idx + 1:]:
                p(f"ADD_{value}", larger_sym, f"ADD_{larger_value - value}", "_", "R")
                seen_values.setdefault(larger_value - value, set())
                seen_values.setdefault(value, set()).add(larger_sym)

        for value, dont_ignore in seen_values.items():
            p.find(f"ADD_{value}", "_", (NUMERAL_SYMBOLS - dont_ignore) | {"|"}, "R", f"ADD_{value - 1}" if value != 1 else "NEXT", "|", "R" if value != 1 else "L")

        for value in range(1, max(seen_values.keys())):
            if value in seen_values:
                continue
            p.find(f"ADD_{value}", "_", "", "R", f"ADD_{value - 1}" if value != 1 else "NEXT", "|", "R")

        p.find("NEXT", "_", {*NUMERAL_SYMBOLS, "|"}, "L", "INIT", "_", "R")
        p("INIT", "|", "HALT", "|", "L")



if __name__ == "__main__":
    main()
