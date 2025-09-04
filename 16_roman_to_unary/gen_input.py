def int_to_roman(num: int) -> str:
    if not (1 <= num <= 3999):
        raise ValueError("Number out of range (must be 1..3999)")

    values = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
    symbols = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]

    roman = []
    for v, s in zip(values, symbols):
        count, num = divmod(num, v)
        roman.append(s * count)
    return "".join(roman)


def main() -> None:
    with open("input.txt", "w") as f:
        for n in range(1, 4000):
            print(f"{int_to_roman(n)} => {'|' * n}", file=f)


if __name__ == "__main__":
    main()
