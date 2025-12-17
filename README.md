# FinanceAdm (Initial Version)

A lightweight, modular CLI personal finance and administration system written in Python.

**Status:** Initial version — most modules have been tested locally and are working so far. This repository is an early-stage study project and may receive breaking changes during active development.

**Planned next update:** add OFX import support to automatically ingest bank/exported statements.

**Contents**
- `core.py` — domain models and managers (entities, accounts, revenues/expenses, entries)
- `files.py` — JSON persistence helpers
- `tools.py` — input validation helpers
- `menu.py` — simple CLI front-end
- `analysis.py` — report generation (financial summary)
- `install.py` — initial data setup

**Key features**
- Entity, account and revenue/expense modeling
- Year-based entries with opening balances and optional locking
- Text-based financial summary reports (operational, financing, investing results)
- Simple JSON persistence for easy inspection and portability
- Basic input validation utilities and a small unit test suite

**Prerequisites**
- Python 3.10 or newer

**Quick start**
1. Clone this repository or open it in a Codespace.
2. (Optional) Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # Linux / macOS
.\.venv\Scripts\activate   # Windows (PowerShell)
```

3. Initialize core data (creates required JSON files and folders):

```bash
python install.py
```

4. Run the interactive menu to manage entities, accounts, entries and reports:

```bash
python menu.py
```

5. Save files from menu options when requested. Generated reports are written to the `in_out` folder (see `menu.py`).


**Next immediate planned features**
- OFX file import: parse OFX bank/export statements and create entries automatically
- Better error handling and logging

**Notes & contributions**
- This is an initial/study project; behavior and file formats may change.
- Contributions welcome: open an issue or a PR with suggested improvements.