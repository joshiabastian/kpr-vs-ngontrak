import os
import sqlite3
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get paths from .env with fallbacks
SQLITE_DB_PATH = os.getenv("SQLITE_DB_PATH", "./db/kpr_vs_ngontrak_sqlite.db")
SCHEMA_PATH = os.getenv("SCHEMA_PATH", "./db/init_schema_sqlite.sql")
SEED_PATH = os.getenv("SEED_PATH", "./db/seed")


def ensure_directory_exists(filepath):
    """Pastikan directory untuk file exists."""
    directory = os.path.dirname(filepath)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
        print(f"[INFO] Directory created: {directory}")


def get_sqlite_connection():
    """Create SQLite connection with proper error handling."""
    try:
        # Ensure database directory exists
        ensure_directory_exists(SQLITE_DB_PATH)

        conn = sqlite3.connect(SQLITE_DB_PATH)
        conn.execute("PRAGMA foreign_keys = ON")  # Enable foreign key constraints
        print(f"[INFO] SQLite connection successful: {SQLITE_DB_PATH}")
        return conn
    except sqlite3.Error as e:
        print(f"[ERROR] Failed to connect to SQLite: {e}")
        return None


def execute_sql_file(conn, filepath):
    """Execute SQL file with error handling."""
    if not os.path.exists(filepath):
        print(f"[ERROR] File not found: {filepath}")
        return False

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            sql_content = f.read()

        # Execute the SQL script
        conn.executescript(sql_content)
        conn.commit()
        print(f"[INFO] Successfully executed: {filepath}")
        return True

    except Exception as e:
        print(f"[ERROR] Failed to execute {filepath}: {e}")
        conn.rollback()
        return False


def load_seed_data(conn):
    """Load all seed files from seed directory."""
    if not os.path.exists(SEED_PATH):
        print(f"[WARNING] Seed directory not found: {SEED_PATH}")
        return

    # Get all .sql files in seed directory
    seed_files = [f for f in os.listdir(SEED_PATH) if f.endswith('.sql')]

    if not seed_files:
        print(f"[WARNING] No .sql files found in: {SEED_PATH}")
        return

    # Sort files to ensure consistent loading order
    seed_files.sort()

    print(f"[INFO] Loading {len(seed_files)} seed files...")

    for seed_file in seed_files:
        seed_file_path = os.path.join(SEED_PATH, seed_file)
        if execute_sql_file(conn, seed_file_path):
            print(f"[INFO] ✅ Loaded seed: {seed_file}")
        else:
            print(f"[ERROR] ❌ Failed to load seed: {seed_file}")


def check_database_exists():
    """Check if database file already exists."""
    return os.path.exists(SQLITE_DB_PATH)


def init_sqlite_db(force_recreate=False):
    """
    Initialize SQLite database with schema and seed data.

    Args:
        force_recreate (bool): If True, recreate database even if exists
    """
    print("=" * 50)
    print("🚀 SQLite Database Initialization")
    print("=" * 50)

    # Debug info
    print(f"[DEBUG] Database Path: {SQLITE_DB_PATH}")
    print(f"[DEBUG] Schema Path: {SCHEMA_PATH}")
    print(f"[DEBUG] Seed Path: {SEED_PATH}")
    print()

    # Check if database exists
    db_exists = check_database_exists()

    if db_exists and not force_recreate:
        print("[INFO] 📋 Database already exists.")
        user_input = input("Do you want to recreate it? (y/N): ").lower().strip()
        if user_input not in ['y', 'yes']:
            print("[INFO] ⏭️ Skipping initialization.")
            return
        force_recreate = True

    # Remove existing database if force recreate
    if force_recreate and db_exists:
        try:
            os.remove(SQLITE_DB_PATH)
            print(f"[INFO] 🗑️ Removed existing database: {SQLITE_DB_PATH}")
        except Exception as e:
            print(f"[ERROR] Failed to remove existing database: {e}")
            return

    # Create database connection
    conn = get_sqlite_connection()
    if conn is None:
        print("[ERROR] ❌ Failed to establish database connection.")
        return

    try:
        # Step 1: Load schema
        print("\n[STEP 1] 📊 Loading database schema...")
        if not execute_sql_file(conn, SCHEMA_PATH):
            print("[ERROR] ❌ Failed to load schema. Aborting.")
            return

        # Step 2: Load seed data
        print("\n[STEP 2] 🌱 Loading seed data...")
        load_seed_data(conn)

        # Step 3: Verify database
        print("\n[STEP 3] ✅ Verifying database...")
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        if tables:
            print(f"[INFO] ✅ Database created successfully with {len(tables)} tables:")
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
                count = cursor.fetchone()[0]
                print(f"[INFO]   📋 {table[0]}: {count} records")
        else:
            print("[WARNING] ⚠️ No tables found in database.")

        print("\n" + "=" * 50)
        print("🎉 Database initialization completed!")
        print("=" * 50)

    except Exception as e:
        print(f"[ERROR] ❌ Unexpected error during initialization: {e}")

    finally:
        conn.close()
        print("[INFO] 🔌 Database connection closed.")


def reset_database():
    """Reset database by recreating from scratch."""
    init_sqlite_db(force_recreate=True)


if __name__ == "__main__":
    import sys

    # Check command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--reset":
            reset_database()
        elif sys.argv[1] == "--force":
            init_sqlite_db(force_recreate=True)
        else:
            print("Usage:")
            print("  python init_sqlite.py        # Normal initialization")
            print("  python init_sqlite.py --reset # Force reset database")
            print("  python init_sqlite.py --force # Force recreate without asking")
    else:
        init_sqlite_db()