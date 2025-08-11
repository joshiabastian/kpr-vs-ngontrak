import sqlite3

def init_sqlite_db():
    conn = sqlite3.connect(r"D:\analisa-project\github\kpr-vs-ngontrak\db\kpr_vs_ngontrak_sqlite.db")
    with open(r"D:\analisa-project\github\kpr-vs-ngontrak\db\init_schema_sqlite.sql", "r") as f:
        sql = f.read()
        conn.executescript(sql)
    conn.commit()
    conn.close()
    print("✅ SQLite database initialized with schema.")

if __name__ == "__main__":
    init_sqlite_db()
