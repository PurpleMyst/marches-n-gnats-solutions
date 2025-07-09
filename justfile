set windows-shell := ["pwsh.exe", "-NoLogo", "-Command"]

run script opt="":
    python3 {{opt}} "{{script}}"
    cat rules.txt | scb
    python3 mill.py
