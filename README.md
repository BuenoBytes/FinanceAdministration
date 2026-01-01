# FinanceAdministration

# 💰 Small Financial Administration System

A robust, modular Python-based financial management tool designed for personal or small business accounting. This project demonstrates advanced logic in data validation, accounting workflows (like year-end locking), and integration with banking standards (OFX).

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/frontend-Streamlit-FF4B4B.svg)

## 🌟 Key Features

* **Comprehensive Ledger Management:** Record, edit, and track revenues and expenses with categorized entries.
* **OFX Integration:** Automatic parsing and importing of bank statement files (`.ofx`), including a "resolution" workflow for unidentified transactions.
* **Year-End Locking (Lock Year):** A professional accounting feature that prevents modifications to past years and automatically carries forward balances to the next period.
* **Dynamic Financial Reports:** Real-time generation of Income Statements and Cash Flow summaries using custom date intervals.
* **Robust Data Validation:** Custom validation engine to ensure data integrity across all system modules.

## 🏗️ Technical Architecture

The project follows a **Modular Monolith** structure, promoting separation of concerns:

* **`core.py`**: The heart of the system. Contains the business logic, Object-Oriented (OOP) models for Entities, Entries, and Balances, and the accounting engine.
* **`app.py`**: The reactive frontend built with **Streamlit**, handling user interaction and state management.
* **`ofx.py`**: Specialized module for handling external banking data and mapping it to the internal schema.
* **`tools.py`**: A utility layer containing a custom validation class (`ObjCheck`) and secure file management.
* **`install.py`**: Automated setup script to initialize the JSON database schema and default categories.

## 🛠️ Tech Stack

* **Language:** Python 3.10+
* **Interface:** Streamlit (Web-based UI)
* **Data Handling:** Pandas (for reporting) and JSON (for persistence)
* **Parsing:** `ofxparse` for financial data extraction

## 🚀 Getting Started

### Prerequisites
* Python 3.10 or higher
* Pip (Python package manager)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/BuenoBytes/FinanceAdministration
    cd FinanceAdministration
    ```

2.  **Install dependencies:**
    ```bash
    pip install streamlit pandas ofxparse
    ```

3.  **Initialize the system:**
    Run the installer to create the necessary directory structure and configuration files.
    ```bash
    python install.py
    ```

4.  **Run the application:**
    ```bash
    python -m streamlit run app.py
    ```

## 📊 Logic & Design Philosophy

This project was built with a focus on **Data Integrity**. Unlike simple trackers, this system:
1.  Uses **Type Hinting** for better maintainability and code clarity.
2.  Implements **Defensive Programming** via the `tools.ObjCheck` class, ensuring that no invalid strings or out-of-range values corrupt the data files.
3.  Handles **Atomic File Saving**: Data is first written to a temporary file before replacing the original, preventing data loss during potential crashes.

### Contact & Portfolio
Developed by **[BuenoBytes]**(On GitHub).
*Focus: Backend Development, Data Processing, and Financial Logic.*