from utils import SAME, Program

# On the input tape, you'll get a positive unary number that is also a perfect square. Your task is
# to compute its square root.
# For example, if the input tape is `|||||||||`, your output tape should be `|||` (√9 = 3).
# -------------------------------------------------------------------------------------------------
# Solution based on subtracting successive odd numbers.


def main() -> None:
    with Program() as p:
        # Mark the end of the input
        p.find("INIT", "_", "|", "R", "START", "E", "L")

        # Mark the end of the to-be-added state with I, decrementing once as we do so.
        p.find("START", "_", "|", "L", "FIRST_2", "I", "R")
        p("FIRST_2", "|", "NEXT_2", "2", "R")

        # Go to next number to be subtracted
        p.find("NEXT_2", "2", set("|_0"), "L", "SUB_2", "0", "L")

        # Build the subtrahend and subtract it from the input.
        for n in range(2, 256):
            p(f"SUB_{n}", "2", f"SUB_{n + 2}", "0", "L")
            p(f"SUB_{n}", "I", f"SUB_{n}", "I", "R")

            p.find(f"SUB_{n}", "|", set("_0"), "R", f"SUB_{n - 1}", "_", "R")

            p(f"SUB_{n}", "E", "FINISH", "_", "L")

        # Handle the base case of subtracting 1
        p("SUB_1", "|", "NEXT_2", "_", "L")

        # If we get to the end of the input, we should increment the subtrahend and continue.
        p("NEXT_2", "I", "INC", "I", "R")

        # Refresh the zeroes to twos and add another two to the subtrahend.
        p("INC", "0", "INC", "2", "R")
        p("INC", "_", "DEC", "2", "R")

        # Decrement once before continuing, as we store the "even part" of the subtrahend.
        p.find("DEC", "|", "_", "R", "NEXT_2", "_", "L")

        # If we hit the end of the input while subtracting, we are done.
        for state in ("DEC", "NEXT_2"):
            p(state, "E", "FINISH", "_", "L")

        # Clean up the tape and halt.
        p.ignore("FINISH", "_", "L")
        p("FINISH", set("02"), "FINISH", "|", "L")
        p("FINISH", "I", "HALT", "_", "R")


if __name__ == "__main__":
    main()
