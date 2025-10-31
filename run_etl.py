import sqlite3

def execute_sql_file(db_path, sql_path):
    # Read SQL file
    with open(sql_path, 'r') as file:
        sql_script = file.read()
    
    # Connect to database
    print(f"Connecting to database: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Split script into individual statements
    statements = sql_script.split(';')
    
    try:
        # Execute each statement
        for statement in statements:
            if statement.strip():
                print(f"\nExecuting statement:\n{statement.strip()}")
                cursor.execute(statement.strip())
                print("Statement executed successfully")
        
        # Commit changes
        conn.commit()
        print("\nAll statements executed successfully. Changes committed.")
    
    except sqlite3.Error as e:
        print(f"\nAn error occurred: {e}")
        conn.rollback()
        print("Changes rolled back due to error")
    
    finally:
        cursor.close()
        conn.close()
        print("Database connection closed")

# Execute the ETL script
execute_sql_file('hsbc_risk_esg.db', 'sql/etl.sql')
