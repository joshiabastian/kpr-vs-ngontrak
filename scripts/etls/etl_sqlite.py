import sqlite3
import os
from dotenv import load_dotenv

# Load variabel dari .env
load_dotenv()

# Ambil path DB dari .env
DB_PATH = os.getenv("SQLITE_DB_PATH")
if not DB_PATH:
    raise ValueError("SQLITE_DB_PATH belum di-set di file .env")

def run_sql_file(conn, filepath):
    """Jalankan semua query SQL dari file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        sql_script = f.read()
    conn.executescript(sql_script)
    conn.commit()

def etl_sqlite():
    """Inisialisasi DB SQLite, load schema & seed data."""
    print(f"[INFO] Menghubungkan ke database: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)

    # Load schema
    schema_path = os.path.join("db", "init_schema.sql")
    if os.path.exists(schema_path):
        print("[INFO] Memuat schema database...")
        run_sql_file(conn, schema_path)
    else:
        print("[WARNING] Schema file tidak ditemukan!")

    # Load seed data
    seed_path = os.path.join("db", "seed_data.sql")
    if os.path.exists(seed_path):
        print("[INFO] Memuat dummy data...")
        run_sql_file(conn, seed_path)
    else:
        print("[WARNING] Seed data file tidak ditemukan!")

    # Cek tabel
    print("[INFO] Daftar tabel di database:")
    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
    for row in cursor.fetchall():
        print(f" - {row[0]}")

    conn.close()
    print("[INFO] ETL selesai.")

if __name__ == "__main__":
    etl_sqlite()
