import random
from pathlib import Path

def main() -> None:
    with open(Path(__file__).parent / "input.txt", "w", encoding="utf-8") as f:
        for _ in range(1024):
            lhs = random.randint(1, 10)
            rhs = random.randint(1, 10)
            q, r = divmod(lhs, rhs)
            f.write(f"{'|' * lhs}÷{'|' * rhs} => {'|' * q},{'|' * r}\n")



if __name__ == "__main__":
    main()
