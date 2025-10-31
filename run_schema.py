import sqlite3
import pathlib

DB = 'hsbc_risk_esg.db'
SQL = 'sql/schema.sql'

print(f"Using DB: {pathlib.Path(DB).resolve()}")
print(f"Applying SQL file: {pathlib.Path(SQL).resolve()}")

with open(SQL, 'r', encoding='utf-8') as f:
    sql_script = f.read()

conn = sqlite3.connect(DB)
try:
    conn.executescript(sql_script)
    conn.commit()
    print('Schema applied successfully.')
except Exception as e:
    print('Error applying schema:', e)
    conn.rollback()
finally:
    conn.close()
    print('Database connection closed.')
