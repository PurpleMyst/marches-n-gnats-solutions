from pathlib import Path

def main() -> None:
    with open(Path(__file__).parent / "input.txt", "w", encoding="utf-8") as f:
        for lhs in range(1, 10):
            for rhs in range(1, 10):
                q, r = divmod(lhs, rhs)
                f.write(f"{'|' * lhs}÷{'|' * rhs} => {'|' * q},{'|' * r}\n")



if __name__ == "__main__":
    main()
