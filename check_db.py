import sqlite3

def check_tables():
    try:
        # Connect directly to your local SQLite binary file
        conn = sqlite3.connect("business_intelligence.db")
        cursor = conn.cursor()
        
        # Query SQLite's internal master schema for a list of table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print("--- Database Verification ---")
        if tables:
            print("Successfully connected! Found the following tables:")
            for table in tables:
                print(f"✅ Table name: {table[0]}")
        else:
            print("❌ Connected, but no tables found inside the database.")
            
        conn.close()
    except Exception as e:
        print(f"❌ Failed to connect to database: {e}")

if __name__ == "__main__":
    check_tables()