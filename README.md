# 🛒 Sales & Inventory Management API

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?logo=fastapi)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-red?logo=sqlite)
![Pytest](https://img.shields.io/badge/Pytest-Passed-success?logo=pytest)

A robust RESTful API built with **Python** and **FastAPI** designed to handle centralized product management, automated stock synchronization, and core business rules for processing sales.

---

## 🎯 Key Features

- **Product Management:** Complete catalog CRUD capabilities including unit price and stock tracking.
- **Sales Processing & Business Logic:**
  - **Automated Stock Deduction:** Prevents sales transactions if the requested item quantity exceeds available inventory (returns HTTP 400).
  - **Progressive Discounting:** Automatically applies a 5% discount on transactions exceeding $200.00.
  - **Price Integrity:** Freezes the product unit price at the time of sale to maintain accurate historical financial records.
- **Isolated Automated Testing:** Full test suite running on an in-memory SQLite database.

---

## 🛠️ Tech Stack

- **Language:** Python 3.12
- **Web Framework:** FastAPI
- **ASGI Server:** Uvicorn
- **ORM & Database:** SQLAlchemy & SQLite
- **Data Validation:** Pydantic v2
- **Automated Testing:** Pytest & HTTPX (`TestClient`)

---

## 📁 Project Structure

```text
api-gestao-vendas/
│
├── app/
│   ├── __init__.py
│   ├── database.py       # Database connection & session setup (SQLAlchemy)
│   ├── models.py         # Relational database models (ORM)
│   ├── schemas.py        # Data validation & API contracts (Pydantic)
│   ├── crud.py           # Core business logic & persistence operations
│   └── main.py           # HTTP endpoints & API routes
│
├── tests/
│   ├── __init__.py
│   └── test_vendas.py    # Integration & unit test suite
│
├── .gitignore
├── requirements.txt
└── README.md