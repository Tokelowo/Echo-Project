import sqlite3
import os

# Connect to the Django SQLite database
db_path = os.path.join(os.path.dirname(__file__), 'db.sqlite3')

if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if the subscription table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%subscription%';")
    tables = cursor.fetchall()
    print("Subscription-related tables:", tables)
    
    # Try to get subscription count
    try:
        cursor.execute("SELECT COUNT(*) FROM research_agent_reportsubscription WHERE is_active = 1;")
        active_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM research_agent_reportsubscription;")
        total_count = cursor.fetchone()[0]
        
        print(f"\n=== EMAIL SUBSCRIPTION STATUS ===")
        print(f"Total subscriptions: {total_count}")
        print(f"Active subscriptions: {active_count}")
        
        if active_count > 0:
            cursor.execute("""
                SELECT user_email, agent_type, frequency, next_run_date, is_active 
                FROM research_agent_reportsubscription 
                WHERE is_active = 1
                LIMIT 10;
            """)
            subscriptions = cursor.fetchall()
            
            print(f"\nACTIVE SUBSCRIPTIONS:")
            print("-" * 50)
            for sub in subscriptions:
                email, agent_type, frequency, next_run, active = sub
                print(f"Email: {email}")
                print(f"Type: {agent_type}")
                print(f"Frequency: {frequency}")
                print(f"Next delivery: {next_run}")
                print(f"Active: {active}")
                print("-" * 30)
        else:
            print("\n❌ No active subscriptions found!")
            print("This is why you didn't receive daily emails.")
            print("\nTo fix this, you need to:")
            print("1. Subscribe through the web app, OR")
            print("2. Run: python setup_daily_subscription.py")
            
    except Exception as e:
        print(f"Error querying subscriptions: {e}")
    
    conn.close()
else:
    print(f"Database not found at: {db_path}")
