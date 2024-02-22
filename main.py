from flask import Flask, request
from datetime import datetime
from prometheus_flask_exporter import PrometheusMetrics
import sqlite3

app = Flask(__name__)
metrics = PrometheusMetrics(app)

DATABASE = '/app/users.db'

def log_user_request(name):
    timestamp = datetime.now().strftime("%H:%M:%S - %d.%m.%Y")
    log_entry = f"name: {name} - {timestamp}\n"
    
    with open("/app/user_log.txt", "a") as log_file:
        log_file.write(log_entry)

def create_user_table():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_user_data(name):
    timestamp = datetime.now().strftime("%H:%M:%S - %d.%m.%Y")
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (name, timestamp) VALUES (?, ?)', (name, timestamp))
    conn.commit()
    conn.close()

@app.route('/hello', methods=['GET'])
def hello():
    return 'Hello Page'

@app.route('/user', methods=['POST'])
def user():
    name = request.args.get('name', '')
    log_user_request(name)
    
    if app.config['USE_SQLITE']:
        create_user_table()
        insert_user_data(name)
    
    return f"User {name} logged."

@app.route('/user', methods=['GET'])
def tail():
    name = request.args.get('name', '')
    return name
    
    if not user:
        return 'Error: Name parameter is missing.', 400
    
    if app.config['USE_SQLITE']:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE name = ?', (name,))
        result = cursor.fetchall()
        conn.close()
        return str(result)

@app.route('/metrics')
def metrics_endpoint():
    return metrics.generate_metrics()

if __name__ == '__main__':
    app.config['USE_SQLITE'] = False  # Change to True to use SQLite
    app.run(host="0.0.0.0", port=80)