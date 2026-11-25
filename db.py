import os
import psycopg
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")


def get_conn():
    return psycopg.connect(DATABASE_URL)


def init_db():
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS applications (
                id SERIAL PRIMARY KEY,
                company TEXT NOT NULL,
                role TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'applied',
                applied_on DATE DEFAULT CURRENT_DATE,
                updated_at TIMESTAMP DEFAULT NOW()
            )
        """)


def add_application(company, role, status="applied"):
    with get_conn() as conn:
        row = conn.execute(
            "INSERT INTO applications (company, role, status) "
            "VALUES (%s, %s, %s) RETURNING id",
            (company, role, status),
        ).fetchone()
    return row[0]


def update_status(company, status):
    with get_conn() as conn:
        cur = conn.execute(
            "UPDATE applications SET status = %s, updated_at = NOW() "
            "WHERE company ILIKE %s",
            (status, f"%{company}%"),
        )
    return cur.rowcount


def get_stats():
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT status, COUNT(*) FROM applications GROUP BY status"
        ).fetchall()
    return {status: count for status, count in rows}