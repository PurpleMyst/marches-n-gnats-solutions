from utils import Program

# On the input tape, you'll get a positive unary number that is also a perfect
# square.    Your task is to compute its square root.
# For example, if the input tape is `|||||||||`, your output tape should be `|||` (√9 = 3).

def main() -> None:
    with Program() as p:
        # p("INIT", "|", "INIT", "|", "L")
        p.find("INIT", "_", "|", "R", "INIT0", "E", "L")
        p.find("INIT0", "_", "|", "L", "INIT2", "_", "L")
        p("INIT2", "_", "INIT3", "!", "L")
        p("INIT3", "_", "SUB", "I", "R")

        p.find("SUB", "!", set("|_j"), "L", "DO_SUB", "j", "R")
        p("SUB", "I", "INC", "!", "L")
        p("INC", "_", "INC2", "!", "L")
        p("INC2", "_", "SUJ", "I", "R")
        p.ignore("SUJ", "!", "R")
        p("SUJ", "j", "SUJ", "!", "R")
        p("SUJ", "_", "SUB", "_", "L")
        p.find("DO_SUB", "|", set("_j"), "R", "SUB", "_", "L")
        p("DO_SUB", "E", "FINISH", "_", "L")

        p.find("FINISH", "j", "_", "L", "FINISH2", "_", "L")
        p("FINISH2", set("j!"), "INCFINISH", "_", "L")
        p.find("INCFINISH", "I", set("j!|"), "L", "FINISH3", "|", "L")
        p("FINISH3", "_", "FINISH4", "I", "R")
        p.find("FINISH4", "_", set("j|I!"), "R", "FINISH5", "_", "L")
        p.find("FINISH5", set("j!"), "_", "L", "FINISH2", "_", "L")

        p.ignore("FINISH2", "|", "L")
        p("FINISH2", "I", "HALT", "_", "L")


if __name__ == "__main__":
    main()
