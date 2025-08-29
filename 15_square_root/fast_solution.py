from utils import build_safe_charset, Program, SAME

# On the input tape, you'll get a positive unary number that is also a perfect square. Your task is
# to compute its square root.
# For example, if the input tape is `|||||||||`, your output tape should be `|||` (√9 = 3).
# -------------------------------------------------------------------------------------------------
# Solution based on subtracting successive odd numbers, but faster.

MAX_N = 256

def main() -> None:
    # Get a safe charset (i.e. printable UTF-8 characters) that'll be used in the program, this'll
    # represent the numbers from 0 to MAX_N.
    cs = build_safe_charset()[500:]

    with Program() as p:
        # Mark the end of the input tape.
        p.find("INIT", "_", "|", "R", "START", "E", "L")

        # Move back to the beginning of the tape, decrement once and move on to subtracting two.
        p.find("START", "_", "|", "L", "FIRST_2", "_", "R")
        p("FIRST_2", "|", "SUB_2", cs[2], "R")

        # Each SUB_n state removes a "|" from the tape and transitions to SUB_(n-1) until n=1, when
        # it transitions to INC to increment the result counter. If there aren't enough "|"s to
        # subtract n, it transitions to FINISH to finalize the result.
        for n in range(2, MAX_N):
            p.find(f"SUB_{n}", "|", set("_0"), "R", f"SUB_{n - 1}", "_", "R")
            p(f"SUB_{n}", "E", "FINISH", "_", "L")
        p("SUB_1", "|", "INC", "_", "L")

        # The INC state finds the current counter value, increments it and moves it closer to the
        # remaining input tape.
        for n in range(2, MAX_N):
            p.find("INC", cs[n], set("_"), "L", f"DEC_{n}", "_", "R")
            p.find(f"DEC_{n}", "|", "_", "R", f"SUB_{n + 2}", cs[n + 2], "R")

        # The FINISH state removes the counter value from the tape and writes out half of it as the
        # final result (since the counter will have value 2sqrt(n) + 1 at the end).
        for n in range(2, MAX_N):
            p.find("FINISH", cs[n], "_", "L", f"DROP_{n // 2 - 1}" if n // 2 != 1 else "HALT", "|", "L")
        for n in range(1, MAX_N):
            p(f"DROP_{n}", "_", f"DROP_{n - 1}" if n != 1 else "HALT", "|", "L")


if __name__ == "__main__":
    main()
