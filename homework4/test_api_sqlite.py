import requests
import sqlite3
import json
import time
from datetime import datetime

# -------- Configuration --------
BASE_URL = "http://127.0.0.1:8000"
QUERY_LIST = [
    "transformer model",
    "attention mechanism",
    "LLMs in NLP",
    "BERT vs GPT"
]
DB_PATH = "search_logs.db"

# -------- Initialize SQLite DB --------
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS search_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT,
            document TEXT,
            chunk TEXT,
            elapsed REAL,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

# -------- Save Log to DB --------
def save_log(query, document, chunk, elapsed):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO search_logs (query, document, chunk, elapsed, timestamp)
        VALUES (?, ?, ?, ?, ?)
    ''', (query, document, chunk, elapsed, datetime.now().isoformat()))
    conn.commit()
    conn.close()

# -------- Send Search Request --------
def send_search(query):
    url = f"{BASE_URL}/search"
    headers = {"Content-Type": "application/json"}
    payload = {"q": query}
    
    start = time.time()
    response = requests.post(url, headers=headers, json=payload)
    elapsed = round(time.time() - start, 4)
    
    if response.status_code == 200:
        data = response.json()
        for result in data.get("results", []):
            document = result.get("document")
            chunk = result.get("chunk", "")[:200]  # Save first 200 chars only
            save_log(query, document, chunk, elapsed)
            print(f"✅ {query} → {document} ({elapsed}s)")
    else:
        print(f"❌ Failed for '{query}': {response.status_code} {response.text}")

# -------- Run All Tests --------
if __name__ == "__main__":
    init_db()
    for query in QUERY_LIST:
        send_search(query)
