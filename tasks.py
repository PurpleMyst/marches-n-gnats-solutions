# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "argdantic",
#     "argh",
#     "bs4",
#     "prompt-toolkit",
#     "pyfzf",
#     "pyhtml2md",
#     "pyperclip",
#     "requests",
#     "unidecode",
#     "pretty_errors",
# ]
# ///
import os
import re
import subprocess
import sys
import webbrowser
from glob import glob
from pathlib import Path

import pretty_errors as _
import pyfzf
import pyhtml2md
import requests
import unidecode
from argh import aliases, dispatch_commands
from bs4 import BeautifulSoup


@aliases("r")
def run(quest: str, pattern: str = "", compress: bool = False, quiet: bool = False) -> None:
    if quest.isdigit():
        [quest_path] = Path(__file__).parent.glob(f"*{quest}*")
        quest = quest_path.name

    quest_dir = Path(__file__).parent / quest
    py_files = list(quest_dir.glob("*.py"))
    match py_files:
        case [py_file]:
            py_file = py_file.resolve()
        case []:
            raise FileNotFoundError(f"No Python file found in {quest_dir}")
        case _:
            [py_file] = pyfzf.FzfPrompt().prompt(
                [p.resolve().name for p in py_files],
                "--reverse --height=30%" + f" --filter={pattern}" if pattern else "",
            )
            py_file = Path(quest_dir, py_file).resolve()
    print(f"Running quest {quest} with python file {py_file.name}")

    input_file = py_file.parent / "input.txt"
    if input_file.exists():
        args = ["-i", input_file]  # type: ignore
    else:
        args = []
    if compress:
        args.append("-c")
    if quiet:
        args.append("-q")

    env = os.environ.copy()
    env["PYTHONPATH"] = str(Path(__file__).parent)
    try:
        subprocess.run(
            [sys.executable, str(py_file)] + list(args),
            env=env,
        )
    except KeyboardInterrupt:
        print("Execution interrupted by user.")


def is_solved(quest: str) -> bool:
    return bool(glob("*" + format(int(re.search(r"/quest/(\d+)", quest).group(1)), "02") + "*"))


@aliases("ss")
def start_solve() -> None:
    os.chdir(Path(__file__).parent)
    base_url = "https://mng.quest"
    resp = requests.get(base_url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    quests = [base_url + a["href"] for a in soup.find_all("a", href=re.compile(r"^/quest/\d+"))]
    unsolved_quests = [q for q in quests if not is_solved(q)]
    if not unsolved_quests:
        print("All quests are solved!")
        return
    print("Unsolved quests:")
    for quest in unsolved_quests:
        quest_id = re.search(r"/quest/(\d+)", quest).group(1)
        print(f"  {quest_id}: {quest}")
    fzf = pyfzf.FzfPrompt()
    [quest_id] = fzf.prompt(unsolved_quests, "--reverse --multi --height=30%")

    quest_num, quest_name = re.search(r"/quest/(\d+)/([^/]+)", quest_id).groups()
    quest_dir = Path(__file__).parent / f"{int(quest_num):02}_{quest_name.replace('-', '_')}"
    if not quest_dir.exists():
        print(f"Quest directory {quest_dir} does not exist. Creating it.")
        quest_dir.mkdir(parents=True, exist_ok=True)

    quest_url = f"https://mng.quest/quest/{quest_num}/{quest_name}"
    quest_resp = requests.get(quest_url)
    quest_resp.raise_for_status()
    quest_soup = BeautifulSoup(quest_resp.text, "html.parser")
    task = quest_soup.find(id="task")
    task_lines = pyhtml2md.convert(str(task)).splitlines()
    task_lines = [
        "# " + unidecode.unidecode(line.strip(), errors="preserve")
        for line in task_lines
        if line.strip()
    ]

    (quest_dir / "base_solution.py").write_text(
        "\n".join(
            [
                "from utils import Program",
                "",
                *task_lines,
                "",
                "def main() -> None:",
                "    with Program() as p:",
                "        # Write your solution here",
                "        pass",
                "",
                'if __name__ == "__main__":',
                "    main()",
            ]
        ),
        encoding="utf-8",
    )
    print(f"Created quest directory {quest_dir}.")
    webbrowser.open_new(quest_url)


def main():
    dispatch_commands([run, start_solve])


if __name__ == "__main__":
    main()
