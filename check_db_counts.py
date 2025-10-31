import sqlite3
conn = sqlite3.connect('hsbc_risk_esg.db')
cur = conn.cursor()
for name in ['esg_data','financial_data','risk_labels']:
    try:
        cur.execute(f"SELECT COUNT(*) FROM {name}")
        print(name, cur.fetchone()[0])
    except Exception as e:
        print(name, 'error', e)
try:
    cur.execute('SELECT COUNT(*) FROM merged_data_view')
    print('merged_data_view', cur.fetchone()[0])
except Exception as e:
    print('merged_data_view error', e)
conn.close()
