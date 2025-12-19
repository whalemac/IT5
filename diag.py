try:
    from models import database
    print("Database module imported successfully")
except ImportError as e:
    print(f"Failed to import database: {e}")
except Exception as e:
    print(f"Error importing database: {e}")

try:
    import mysql.connector
    print("mysql.connector imported successfully")
except ImportError:
    print("mysql.connector NOT installed")
