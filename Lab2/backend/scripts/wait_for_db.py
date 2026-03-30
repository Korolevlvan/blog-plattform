import os
import time
import psycopg2

database_url = os.getenv("DATABASE_URL")
if not database_url:
    raise RuntimeError("DATABASE_URL is not set")

for attempt in range(30):
    try:
        conn = psycopg2.connect(database_url)
        conn.close()
        print("Database is ready")
        break
    except Exception as exc:
        print(f"Waiting for database... attempt={attempt+1} error={exc}")
        time.sleep(2)
else:
    raise RuntimeError("Database is not ready after waiting")
