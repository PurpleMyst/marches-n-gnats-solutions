# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "argh",
#     "bs4",
#     "requests",
#     "pyperclip",
#     "argdantic",
# ]
# ///
from argh import dispatch_commands
import requests
from bs4 import BeautifulSoup
from glob import glob
from pathlib import Path
import sys
import os
import subprocess

def run(quest: str, *args: str) -> None:
    if quest.isdigit():
        [quest_path] = Path(__file__).parent.glob(f"{quest}*")
        quest = quest_path.name

    quest_dir = Path(__file__).parent / quest
    py_files = list(quest_dir.glob("*.py"))
    match py_files:
        case [py_file]:
            py_file = py_file.resolve()
        case []:
            raise FileNotFoundError(f"No Python file found in {quest_dir}")
        case _:
            raise ValueError(f"Multiple Python files found in {quest_dir}")
    print(f"Running quest {quest} with python file {py_file.name}")

    input_file = py_file.parent / "input.txt"
    if input_file.exists() and "-i" not in args:
        args = ["-i", input_file, *args]  # type: ignore
    
    env = os.environ.copy()
    env["PYTHONPATH"] = str(Path(__file__).parent)
    subprocess.run(
        [sys.executable, str(py_file)] + list(args),
        env=env,
        check=True,
    )


def main():
    dispatch_commands([run])



if __name__ == "__main__":
    main()
