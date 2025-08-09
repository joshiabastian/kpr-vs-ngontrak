import sqlite3
import glob
import os

# Path database SQLite
DB_PATH = r"D:\bymacho\kpr-vs-ngontrak\db\kpr_vs_ngontrak_sqlite.db"  # sesuaikan sama lokasi file .db lu
# Folder berisi seed SQL
SEED_FOLDER = r"D:\bymacho\kpr-vs-ngontrak\db\seed"

def convert_postgres_to_sqlite(sql):
    """
    Bersihin syntax PostgreSQL supaya aman di SQLite
    """
    # Ganti boolean Postgres ke 0/1
    sql = sql.replace("true", "1").replace("false", "0")
    # Hapus casting Postgres (::)
    import re
    sql = re.sub(r"::\w+", "", sql)
    # Ganti fungsi NOW() ke datetime('now')
    sql = sql.replace("NOW()", "datetime('now')")
    return sql

def run_seed_files():
    # Koneksi ke SQLite
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Cari semua file .sql di folder seed
    seed_files = sorted(glob.glob(os.path.join(SEED_FOLDER, "*.sql")))

    for file_path in seed_files:
        with open(file_path, "r", encoding="utf-8") as f:
            raw_sql = f.read()
            clean_sql = convert_postgres_to_sqlite(raw_sql)
            try:
                cursor.executescript(clean_sql)
                print(f"✅ Berhasil import: {os.path.basename(file_path)}")
            except Exception as e:
                print(f"❌ Gagal import {os.path.basename(file_path)}: {e}")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    run_seed_files()
