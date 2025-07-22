import sqlite3
import os

# Connect to the Django SQLite database
db_path = os.path.join(os.path.dirname(__file__), 'db.sqlite3')

def update_email_time():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Update your email subscriptions to morning delivery
    emails_to_update = ['Temiloluwaokelowo@gmail.com', 't-tokelowo@microsoft.com']
    
    for email in emails_to_update:
        cursor.execute("""
            UPDATE research_agent_reportsubscription 
            SET preferred_time = '09:00',
                next_run_date = '2025-07-16 09:00:00'
            WHERE user_email = ? AND is_active = 1;
        """, (email,))
        
        rows_affected = cursor.rowcount
        print(f"Updated {email}: {rows_affected} subscription(s) -> 9:00 AM delivery")
    
    conn.commit()
    
    # Verify the changes
    print(f"\n=== UPDATED SCHEDULE ===")
    for email in emails_to_update:
        cursor.execute("""
            SELECT user_email, agent_type, frequency, preferred_time, next_run_date 
            FROM research_agent_reportsubscription 
            WHERE user_email = ? AND is_active = 1;
        """, (email,))
        
        sub = cursor.fetchone()
        if sub:
            user_email, agent_type, frequency, pref_time, next_run = sub
            print(f"Email: {user_email}")
            print(f"Type: {agent_type}")
            print(f"Frequency: {frequency}")
            print(f"Preferred time: {pref_time}")
            print(f"Next delivery: {next_run}")
            print("-" * 30)
    
    conn.close()
    print("✅ Email delivery time updated to 9:00 AM!")
    print("You'll receive tomorrow's email at 9:00 AM.")

if __name__ == "__main__":
    update_email_time()
