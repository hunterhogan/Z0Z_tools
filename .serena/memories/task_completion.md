# Task Completion

- Before running any project command, start from the repository root, activate the virtual environment, and then use ordinary commands from the activated environment, such as `pytest`, `python`, `ruff`, or `pyright`.
- This repository's full configured pytest suite runs in less than 5 seconds. Run `pytest` after every change, including docstring-only, type-only, and identifier-only changes.
- Prefer also running `pytest` while making changes to guide the work, not only as a final check.
- If a very narrow affected test target is useful during development, run it first, but still run the full `pytest` suite before finishing.
- Mention any test command that could not run and why.
