import sqlite3

# Connect to (or create) the database file
connection = sqlite3.connect('database.db')

# Create a table to store your 30-minute sessions
with open('schema.sql', 'w') as f:
    connection.execute('''
        CREATE TABLE IF NOT EXISTS workouts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            duration_minutes INTEGER NOT NULL,
            notes TEXT
        );
    ''')

connection.commit()
connection.close()
print("Database initialized successfully!")
