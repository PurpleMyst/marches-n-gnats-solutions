from utils import SAME, Program

ALIVE = "+"
DEAD = "-"

NUMBERS = set("12345")


def main() -> None:
    with Program() as p:
        p("INIT", ALIVE, f"EVOLVE_{1:02b}", min(NUMBERS), "R")
        p("INIT", DEAD, "HALT", "_", "L")

        for state in range(0b100):
            new_state_dead = (state << 1) & 0b10
            new_state_alive = new_state_dead | 0b1
            new_cell_dead = ALIVE if state.bit_count() == 1 else DEAD
            new_cell_alive = ALIVE if state.bit_count() == 0 else DEAD

            p(f"EVOLVE_{state:02b}", DEAD, f"EVOLVE_{new_state_dead:02b}", new_cell_dead, "R")

            p(f"EVOLVE_{state:02b}", ALIVE, f"EVOLVE_{new_state_alive:02b}", new_cell_alive, "R")

            if new_state_dead != 0:
                p(f"EVOLVE_{state:02b}", "_", f"EVOLVE_{new_state_dead:02b}", new_cell_dead, "R")
            elif state != 0:
                p(f"EVOLVE_{state:02b}", "_", f"RETURN", new_cell_dead, "L")

        for n in NUMBERS:
            is_last = n == max(NUMBERS)
            p.find(
                "RETURN",
                n,
                {ALIVE, DEAD},
                "L",
                f"EVOLVE_{1:02b}" if not is_last else "HALT",
                str(int(n) + 1) if not is_last else ALIVE,
                "R",
            )


if __name__ == "__main__":
    main()
