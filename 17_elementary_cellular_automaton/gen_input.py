ALIVE = "+"
DEAD = "-"


def rule22(start, steps=5):
    result = start
    for _ in range(steps):
        new_result = ""
        if result and result[0] == ALIVE:
            new_result += ALIVE
        for i in range(len(result)):
            left = result[i - 1] if i > 0 else DEAD
            center = result[i]
            right = result[i + 1] if i < len(result) - 1 else DEAD

            if (left, center, right) in [
                (DEAD, DEAD, ALIVE),
                (DEAD, ALIVE, DEAD),
                (ALIVE, DEAD, DEAD),
            ]:
                new_result += ALIVE
            else:
                new_result += DEAD
        if result and result[-1] == ALIVE:
            new_result += ALIVE
        result = new_result.strip(DEAD) or "-"
    return result


def main() -> None:
    with open("input.txt", "w") as f:
        seen = set()
        for n in range(1 << 8):
            start = "".join(ALIVE if (n & (1 << i)) else DEAD for i in range(8))
            result = rule22(start)
            start = start.strip(DEAD) or "-"
            result = result.strip(DEAD)
            if (start, result) not in seen:
                seen.add((start, result))
                print(f"{start} => {result}", file=f)


if __name__ == "__main__":
    main()
