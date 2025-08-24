import random
from pathlib import Path


def main() -> None:
    with Path(__file__).parent.joinpath("input.txt").open("a", newline="\n") as f:
        for _ in range(10):
            n = int(random.random() * 1e4)
            f.write(f"{n:b} => {n}\n")


if __name__ == "__main__":
    main()
