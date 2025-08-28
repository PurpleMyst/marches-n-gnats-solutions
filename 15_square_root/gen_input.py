def main() -> None:
    with open("input.txt", "w") as f:
        for n in range(1, 20):
            print(f"{'|' * n**2} =>  {'|' * n}", file=f)


if __name__ == "__main__":
    main()
