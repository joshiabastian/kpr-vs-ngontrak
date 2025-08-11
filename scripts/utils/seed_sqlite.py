import sqlite3
import glob
import os
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get paths from .env with fallbacks
DB_PATH = os.getenv("SQLITE_DB_PATH", "./db/kpr_vs_ngontrak_sqlite.db")
SEED_FOLDER = os.getenv("SEED_PATH", "./db/seed")


def convert_postgres_to_sqlite(sql):
    """
    Convert PostgreSQL syntax to SQLite-compatible syntax
    """
    # Convert PostgreSQL boolean to SQLite integer
    sql = sql.replace("true", "1").replace("false", "0")
    sql = sql.replace("TRUE", "1").replace("FALSE", "0")

    # Remove PostgreSQL type casting (::type)
    sql = re.sub(r"::\w+", "", sql)

    # Replace PostgreSQL functions with SQLite equivalents
    sql = sql.replace("NOW()", "datetime('now')")
    sql = sql.replace("CURRENT_TIMESTAMP", "datetime('now')")
    sql = sql.replace("CURRENT_DATE", "date('now')")

    # Replace PostgreSQL SERIAL with SQLite INTEGER PRIMARY KEY
    sql = re.sub(r"\bSERIAL\b", "INTEGER", sql, flags=re.IGNORECASE)

    # Replace PostgreSQL TEXT with SQLite TEXT (already compatible)
    # Replace DECIMAL with REAL (SQLite doesn't have DECIMAL)
    sql = re.sub(r"\bDECIMAL\(\d+,\d+\)", "REAL", sql, flags=re.IGNORECASE)

    # Remove PostgreSQL-specific constraints that SQLite doesn't support
    sql = re.sub(r"CHECK\s*\([^)]+\)", "", sql, flags=re.IGNORECASE)

    return sql


def validate_seed_folder():
    """Validate that seed folder exists and contains SQL files"""
    if not os.path.exists(SEED_FOLDER):
        print(f"[ERROR] Seed folder not found: {SEED_FOLDER}")
        return False

    sql_files = glob.glob(os.path.join(SEED_FOLDER, "*.sql"))
    if not sql_files:
        print(f"[WARNING] No .sql files found in: {SEED_FOLDER}")
        return False

    print(f"[INFO] Found {len(sql_files)} seed files in: {SEED_FOLDER}")
    return True


def validate_database():
    """Validate that database exists and is accessible"""
    if not os.path.exists(DB_PATH):
        print(f"[ERROR] Database file not found: {DB_PATH}")
        print("[INFO] Run init_sqlite.py first to create the database.")
        return False

    try:
        conn = sqlite3.connect(DB_PATH)
        conn.close()
        print(f"[INFO] Database connection successful: {DB_PATH}")
        return True
    except Exception as e:
        print(f"[ERROR] Cannot connect to database: {e}")
        return False


def run_seed_files():
    """
    Load all seed files from SEED_FOLDER into SQLite database
    with PostgreSQL to SQLite conversion
    """
    print("=" * 50)
    print("🌱 Running Seed Data Import")
    print("=" * 50)

    # Debug info
    print(f"[DEBUG] Database Path: {DB_PATH}")
    print(f"[DEBUG] Seed Folder: {SEED_FOLDER}")
    print()

    # Validate prerequisites
    if not validate_database():
        return False

    if not validate_seed_folder():
        return False

    # Connect to SQLite database
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Enable foreign key constraints
        cursor.execute("PRAGMA foreign_keys = ON")

    except Exception as e:
        print(f"[ERROR] Failed to connect to database: {e}")
        return False

    # Find and sort all SQL files in seed folder
    seed_files = sorted(glob.glob(os.path.join(SEED_FOLDER, "*.sql")))

    success_count = 0
    error_count = 0

    print(f"[INFO] Processing {len(seed_files)} seed files...")
    print()

    for file_path in seed_files:
        file_name = os.path.basename(file_path)

        try:
            # Read SQL file
            with open(file_path, "r", encoding="utf-8") as f:
                raw_sql = f.read()

            # Convert PostgreSQL syntax to SQLite
            clean_sql = convert_postgres_to_sqlite(raw_sql)

            # Execute SQL
            cursor.executescript(clean_sql)
            print(f"[INFO] ✅ Successfully imported: {file_name}")
            success_count += 1

        except Exception as e:
            print(f"[ERROR] ❌ Failed to import {file_name}: {e}")
            error_count += 1
            # Continue with next file instead of stopping

    # Commit changes and close connection
    try:
        conn.commit()
        print(f"\n[INFO] 💾 Changes committed to database.")
    except Exception as e:
        print(f"[ERROR] Failed to commit changes: {e}")
        conn.rollback()
    finally:
        conn.close()
        print(f"[INFO] 🔌 Database connection closed.")

    # Summary
    print("\n" + "=" * 50)
    print("📊 Seed Import Summary")
    print("=" * 50)
    print(f"✅ Successful imports: {success_count}")
    print(f"❌ Failed imports: {error_count}")
    print(f"📁 Total files processed: {len(seed_files)}")

    if error_count == 0:
        print("🎉 All seed files imported successfully!")
    else:
        print("⚠️ Some files failed to import. Check the errors above.")

    return error_count == 0


def dry_run():
    """
    Show what would be converted without actually executing
    """
    print("=" * 50)
    print("🔍 Dry Run - SQL Conversion Preview")
    print("=" * 50)

    if not validate_seed_folder():
        return

    seed_files = sorted(glob.glob(os.path.join(SEED_FOLDER, "*.sql")))

    for file_path in seed_files:
        file_name = os.path.basename(file_path)
        print(f"\n📄 File: {file_name}")
        print("-" * 30)

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                raw_sql = f.read()

            clean_sql = convert_postgres_to_sqlite(raw_sql)

            # Show first few lines of converted SQL
            lines = clean_sql.strip().split('\n')[:5]
            for line in lines:
                if line.strip():
                    print(f"  {line}")

            if len(lines) >= 5:
                print("  ... (truncated)")

        except Exception as e:
            print(f"  ERROR: {e}")


if __name__ == "__main__":
    import sys

    # Check command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--dry-run":
            dry_run()
        else:
            print("Usage:")
            print("  python seed.py           # Import all seed files")
            print("  python seed.py --dry-run # Preview conversion without importing")
    else:
        run_seed_files()