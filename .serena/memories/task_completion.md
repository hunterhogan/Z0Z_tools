# Task Completion

- For test changes, run the narrow affected pytest target first, e.g. `.venv\Scripts\python.exe -m pytest tests\test_autoRevert.py`.
- For syntax-only changes, run `.venv\Scripts\python.exe -m py_compile <path>`.
- If broader behavior changes touch exported package APIs, run `.venv\Scripts\python.exe -m pytest`.
- Mention any test command that could not run and why.