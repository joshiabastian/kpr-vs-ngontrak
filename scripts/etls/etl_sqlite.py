import os
import sqlite3
from dotenv import load_dotenv

# Load .env
load_dotenv()

DB_PATH = os.getenv("SQLITE_DB_PATH")
SCHEMA_PATH = os.getenv("SCHEMA_PATH")
SEED_PATH = os.getenv("SEED_PATH")

def get_sqlite_connection():
    try:
        conn = sqlite3.connect(DB_PATH)
        print(f"[INFO] Koneksi SQLite berhasil: {DB_PATH}")
        return conn
    except sqlite3.Error as e:
        print(f"[ERROR] Gagal konek SQLite: {e}")
        return None

def run_sql_file(conn, filepath):
    """Jalankan semua query SQL dari file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        sql_script = f.read()
    conn.executescript(sql_script)
    conn.commit()
    print(f"[INFO] Berhasil eksekusi: {filepath}")

def initialize_database():
    """Buat DB baru kalau belum ada, lalu load schema & seed."""
    is_new_db = not os.path.exists(DB_PATH)

    conn = get_sqlite_connection()
    if conn is None:
        return

    if is_new_db:
        print("[INFO] Database baru dibuat, inisialisasi schema & seed...")
        run_sql_file(conn, SCHEMA_PATH)

        # Load semua file seed di folder SEED_PATH
        for file_name in sorted(os.listdir(SEED_PATH)):
            if file_name.endswith(".sql"):
                file_path = os.path.join(SEED_PATH, file_name)
                run_sql_file(conn, file_path)
        print("[INFO] Schema & seed selesai di-load.")
    else:
        print("[INFO] Database sudah ada, skip inisialisasi.")

    conn.close()
    print("[INFO] Koneksi ditutup.")

if __name__ == "__main__":
    initialize_database()
