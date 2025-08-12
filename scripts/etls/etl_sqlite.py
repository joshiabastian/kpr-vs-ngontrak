import os
import sqlite3
from dotenv import load_dotenv
import sys

# Load .env
load_dotenv()

# Fallback values kalau .env kosong

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(script_dir, "../..")  # Go up 2 levels

DB_PATH = os.path.join(project_root, "db", "kpr_vs_ngontrak_sqlite.db")
SCHEMA_PATH = os.path.join(project_root, "db", "init_schema.sql")
SEED_PATH = os.path.join(project_root, "db", "seed")

def ensure_directory_exists(filepath):
    """Pastikan directory untuk file exists."""
    directory = os.path.dirname(filepath)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
        print(f"[INFO] Directory dibuat: {directory}")


def get_sqlite_connection():
    try:
        # Pastikan directory database ada
        ensure_directory_exists(DB_PATH)

        conn = sqlite3.connect(DB_PATH)
        print(f"[INFO] Koneksi SQLite berhasil: {DB_PATH}")
        return conn
    except sqlite3.Error as e:
        print(f"[ERROR] Gagal konek SQLite: {e}")
        return None


def run_sql_file(conn, filepath):
    """Jalankan semua query SQL dari file."""
    if not os.path.exists(filepath):
        print(f"[ERROR] File tidak ditemukan: {filepath}")
        return False

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            sql_script = f.read()
        conn.executescript(sql_script)
        conn.commit()
        print(f"[INFO] Berhasil eksekusi: {filepath}")
        return True
    except Exception as e:
        print(f"[ERROR] Gagal eksekusi {filepath}: {e}")
        return False


def initialize_database():
    """Buat DB baru kalau belum ada, lalu load schema & seed."""
    # Debug info
    print(f"[DEBUG] DB_PATH: {DB_PATH}")
    print(f"[DEBUG] SCHEMA_PATH: {SCHEMA_PATH}")
    print(f"[DEBUG] SEED_PATH: {SEED_PATH}")

    is_new_db = not os.path.exists(DB_PATH)

    conn = get_sqlite_connection()
    if conn is None:
        return

    if is_new_db:
        print("[INFO] Database baru dibuat, inisialisasi schema & seed...")

        # Load schema
        if not run_sql_file(conn, SCHEMA_PATH):
            print("[ERROR] Gagal load schema, berhenti.")
            conn.close()
            return

        # Load semua file seed di folder SEED_PATH
        if os.path.exists(SEED_PATH):
            seed_files = [f for f in os.listdir(SEED_PATH) if f.endswith(".sql")]
            for file_name in sorted(seed_files):
                file_path = os.path.join(SEED_PATH, file_name)
                run_sql_file(conn, file_path)
            print("[INFO] Schema & seed selesai di-load.")
        else:
            print(f"[WARNING] Seed directory tidak ditemukan: {SEED_PATH}")
    else:
        print("[INFO] Database sudah ada, skip inisialisasi.")

    conn.close()
    print("[INFO] Koneksi ditutup.")


if __name__ == "__main__":
    initialize_database()