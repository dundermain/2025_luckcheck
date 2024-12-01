from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# MySQL connection configuration
db_config = {
    'host': 'your-mysql-host',
    'user': 'your-username',
    'password': 'your-password',
    'database': 'birth_rankings'
}

@app.route('/get-ranking', methods=['POST'])
def get_ranking():
    data = request.json
    birth_month = data['birthMonth']
    birth_day = data['birthDay']

    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        query = "SELECT ranking FROM rankings WHERE birthMonth = %s AND birthDay = %s"
        cursor.execute(query, (birth_month, birth_day))
        result = cursor.fetchone()
        cursor.close()
        connection.close()

        if result:
            return jsonify({'ranking': result[0]})
        else:
            return jsonify({'ranking': 'No ranking found'}), 404

    except Error as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
