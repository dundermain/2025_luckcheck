from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Create a database connection and table
def init_db():
    conn = sqlite3.connect('rankings.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS rankings (
        birthMonth INTEGER,
        birthDay INTEGER,
        ranking TEXT
    )''')
    conn.commit()
    conn.close()

@app.route('/get-ranking', methods=['POST'])
def get_ranking():
    data = request.json
    birth_month = data['birthMonth']
    birth_day = data['birthDay']

    conn = sqlite3.connect('rankings.db')
    c = conn.cursor()
    c.execute("SELECT ranking FROM rankings WHERE birthMonth = ? AND birthDay = ?", (birth_month, birth_day))
    result = c.fetchone()
    conn.close()

    if result:
        return jsonify({'ranking': result[0]})
    else:
        return jsonify({'ranking': 'No ranking found'}), 404

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
