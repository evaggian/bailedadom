# setup_db.py
import sqlite3

# Function to connect to the SQLite database
def get_db_connection(db_name='database.db'):
    # Connects to the SQLite database file, creates it if it doesn't exist
    conn = sqlite3.connect(db_name)
    return conn

# Function to create the Users and Students tables
def create_tables(conn):
    cursor = conn.cursor()

    # SQL command to create the Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            last_name TEXT,
            email TEXT,
            phone_number NUMERIC
        )
    ''')

    # SQL command to create the Students table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            level SMALLINT,
            role TEXT,
            has_paid BOOLEAN,
            paid_amount INTEGER,
            registered_classes TEXT,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES Users (id)
        )
    ''')

    conn.commit()  # Save changes to the database
    print("Tables created successfully.")

# Main function to set up the database
def setup_database():
    conn = get_db_connection()  # Connect to the database
    create_tables(conn)         # Create the necessary tables
    conn.close()                # Close the database connection

if __name__ == '__main__':
    setup_database()  # Run the setup function
