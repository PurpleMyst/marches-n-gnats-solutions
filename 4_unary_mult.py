from functools import partial

MAX_N = 21


def main() -> None:
    with open("rules.txt", "w", newline="\n") as f:
        print = partial(__builtins__.print, file=f)

        print("INIT | L_1 _ R")

        for n in range(1, MAX_N + 1):
            print(f"L_{n} | L_{n + 1} _ R")

            if n != 1:
                print(f"L_{n} * R_{n}_0 _ R")
            else:
                print(f"L_{n} * HALT _ R")

        for n in range(1, MAX_N + 1):
            for m in range(1, MAX_N + 1):
                print(f"R_{n}_{m - 1} | R_{n}_{m} | R")

                if n - 1 > 0 and m - 2 > 0:
                    print(f"R_{n}_{m - 1} _ M_{n - 1}_{m - 1}_{m - 2} | R")
                elif m == 2 and n - 2 > 0:
                    print(f"R_{n}_{m - 1} _ M_{n - 2}_{m - 1}_{m - 1} | R")
                else:
                    print(f"R_{n}_{m - 1} _ HALT _ R")

        for n in range(1, MAX_N + 1):
            for m in range(1, MAX_N + 1):
                for s in range(1, MAX_N + 1):
                    if n - 1 > 0 and m - 2 > 0:
                        print(f"M_{n - 1}_{s}_{m - 1} _ M_{n - 1}_{s}_{m - 2} | R")
                    elif n - 2 > 0:
                        print(f"M_{n - 1}_{s}_{m - 1} _ M_{n - 2}_{s}_{s} | R")
                    else:
                        print(f"M_{n - 1}_{s}_{m - 1} _ HALT | R")


if __name__ == "__main__":
    main()
