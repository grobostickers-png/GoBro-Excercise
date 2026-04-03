from flask import Flask, render_template, send_from_directory, request, jsonify
import os
import sqlite3

# CRITICAL: This variable must be named 'app' for gunicorn app:app to work
app = Flask(__name__)

# --- Database Setup ---
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS workouts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            duration_minutes INTEGER
        )
    ''')
    conn.commit()
    conn.close()

# Initialize the DB when the script starts
init_db()

# --- PWA & Service Worker Routes ---
# These must be served from the root to have full scope control
@app.route('/sw.js')
def serve_sw():
    return send_from_directory(os.getcwd(), 'sw.js', mimetype='application/javascript')

@app.route('/manifest.json')
def serve_manifest():
    return send_from_directory('static', 'manifest.json')

# --- Main App Routes ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/log', methods=['POST'])
def log_workout():
    data = request.json
    duration = data.get('minutes', 30)
    
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO workouts (duration_minutes) VALUES (?)', (duration,))
        conn.commit()
        conn.close()
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# --- Render Production Config ---
if __name__ == '__main__':
    # Render provides a PORT environment variable
    port = int(os.environ.get("PORT", 5000))
    # host='0.0.0.0' is required for Render to see the app
    app.run(host='0.0.0.0', port=port)