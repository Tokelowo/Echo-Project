import sqlite3
import os
from datetime import datetime

db_path = 'db.sqlite3'
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if the table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND (name LIKE '%subscription%' OR name LIKE '%email%');")
    tables = cursor.fetchall()
    print('Available tables with subscription/email:', tables)
    
    # Try to find the correct table
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    all_tables = cursor.fetchall()
    print('All tables:', [t[0] for t in all_tables])
    
    # Check for research_agent_reportsubscription specifically
    try:
        cursor.execute("SELECT * FROM research_agent_reportsubscription LIMIT 5;")
        rows = cursor.fetchall()
        print('Found research_agent_reportsubscription table with', len(rows), 'rows')
        
        # Get column names
        cursor.execute("PRAGMA table_info(research_agent_reportsubscription);")
        columns = cursor.fetchall()
        print('Columns:', [col[1] for col in columns])
        
        # Show current subscriptions
        cursor.execute("SELECT * FROM research_agent_reportsubscription;")
        subs = cursor.fetchall()
        for sub in subs:
            print('Subscription:', sub)
            
    except Exception as e:
        print('Error accessing research_agent_reportsubscription:', e)
    
    conn.close()
else:
    print('Database file not found!')
