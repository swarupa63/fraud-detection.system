from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app = FastAPI()

# DB connect
conn = sqlite3.connect("fraud.db", check_same_thread=False)
cursor = conn.cursor()

# Table create
cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL,
    status TEXT
)
""")

conn.commit()

class Transaction(BaseModel):
    amount: float

# Fraud check API
@app.post("/check")
def check_fraud(data: Transaction):
    if data.amount > 5000:
        status = "FRAUD DETECTED"
    else:
        status = "NORMAL TRANSACTION"

    # Save to DB
    cursor.execute(
        "INSERT INTO transactions (amount, status) VALUES (?, ?)",
        (data.amount, status)
    )
    conn.commit()

    return {"status": status}

# View all data API
@app.get("/transactions")
def get_transactions():
    cursor.execute("SELECT * FROM transactions")
    rows = cursor.fetchall()

    return {"data": rows}