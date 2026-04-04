from flask import Flask, render_template, send_from_directory, request, jsonify
from flask_cors import CORS
import os
import sqlite3

app = Flask(__name__)
# This is the magic line that allows your PWA to talk to Render securely
CORS(app) 

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # Upgraded to include the date and day sent from your new frontend
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS workouts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            duration_minutes INTEGER,
            workout_date TEXT,
            workout_day TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/sw.js')
def serve_sw():
    return send_from_directory(os.getcwd(), 'sw.js', mimetype='application/javascript')

@app.route('/manifest.json')
def serve_manifest():
    return send_from_directory('static', 'manifest.json')

@app.route('/')
def index():
    return """
    <html>
        <body style="font-family: sans-serif; text-align: center; padding-top: 50px; background-color: #f4f4f9;">
            <h1 style="color: #2c3e50;">🎉 Your Workout Backend is Live!</h1>
            <p style="color: #7f8c8d; font-size: 1.2em;">The server is running perfectly with CORS enabled.</p>
        </body>
    </html>
    """

@app.route('/api/log', methods=['POST'])
def log_workout():
    data = request.json
    duration = data.get('minutes', 30)
    # Catch the new date and day fields
    date = data.get('date', 'Unknown')
    day = data.get('day', 'Unknown')
    
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO workouts (duration_minutes, workout_date, workout_day) VALUES (?, ?, ?)', 
            (duration, date, day)
        )
        conn.commit()
        conn.close()
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)