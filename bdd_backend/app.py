# flask-backend/app.py
from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

# Function to connect to the SQLite database
def get_db_connection():
    conn = sqlite3.connect('db.sqlite3')  # SQLite database file
    conn.row_factory = sqlite3.Row
    return conn

# Initialize the database and create tables
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            last_name TEXT,
            email TEXT,
            phone_number NUMERIC
        )
    ''')

    # Create Students table
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

    conn.commit()
    conn.close()

# Test endpoint to check if the server is running
@app.route('/')
def index():
    return "Flask server is running with SQLite!"

# Example endpoint to add a new user
@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO Users (first_name, last_name, email, phone_number) VALUES (?, ?, ?, ?)',
        (data['first_name'], data['last_name'], data['email'], data['phone_number'])
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "User added successfully!"}), 201

if __name__ == '__main__':
    init_db()  # Initialize the database and create tables
    app.run(debug=True)
