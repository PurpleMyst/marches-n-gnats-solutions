from utils import Program

MAX_N = 21


def main() -> None:
    with Program() as p:
        p(*"INIT | L_1 _ R".split(" "))

        for n in range(1, MAX_N + 1):
            p(*f"L_{n} | L_{n + 1} _ R".split(" "))

            if n != 1:
                p(*f"L_{n} * R_{n}_0 _ R".split(" "))
            else:
                p(*f"L_{n} * HALT _ R".split(" "))

        for n in range(1, MAX_N + 1):
            for m in range(1, MAX_N + 1):
                p(*f"R_{n}_{m - 1} | R_{n}_{m} | R".split(" "))

                if n - 1 > 0 and m - 2 > 0:
                    p(*f"R_{n}_{m - 1} _ M_{n - 1}_{m - 1}_{m - 2} | R".split(" "))
                elif m == 2 and n - 2 > 0:
                    p(*f"R_{n}_{m - 1} _ M_{n - 2}_{m - 1}_{m - 1} | R".split(" "))
                else:
                    p(*f"R_{n}_{m - 1} _ HALT _ R".split(" "))

        for n in range(1, MAX_N + 1):
            for m in range(1, MAX_N + 1):
                for s in range(1, MAX_N + 1):
                    if n - 1 > 0 and m - 2 > 0:
                        p(
                            *f"M_{n - 1}_{s}_{m - 1} _ M_{n - 1}_{s}_{m - 2} | R".split(
                                " "
                            )
                        )
                    elif n - 2 > 0:
                        p(*f"M_{n - 1}_{s}_{m - 1} _ M_{n - 2}_{s}_{s} | R".split(" "))
                    else:
                        p(*f"M_{n - 1}_{s}_{m - 1} _ HALT | R".split(" "))


if __name__ == "__main__":
    main()
