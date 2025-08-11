import os
import sqlite3
from dotenv import load_dotenv

# Load variabel dari .env
load_dotenv()

DB_PATH = os.getenv("SQLITE_DB_PATH")

def get_sqlite_connection():
    """Buat koneksi ke database SQLite berdasarkan path di .env"""
    try:
        conn = sqlite3.connect(DB_PATH)
        print(f"[INFO] Koneksi SQLite berhasil: {DB_PATH}")
        return conn
    except sqlite3.Error as e:
        print(f"[ERROR] Gagal konek SQLite: {e}")
        return None

# Tes koneksi jika file ini dijalankan langsung
if __name__ == "__main__":
    conn = get_sqlite_connection()
    if conn:
        conn.close()
        print("[INFO] Koneksi ditutup.")
