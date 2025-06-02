from flask import Flask, request, jsonify
import pyodbc
import os

app = Flask(__name__)

# Konfiguracja połączenia - dane z App Service
def get_db():
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        f"SERVER={os.environ['DB_SERVER']};"
        f"DATABASE={os.environ['DB_NAME']};"
        f"UID={os.environ['DB_USER']};"
        f"PWD={os.environ['DB_PASSWORD']};"
        "Encrypt=yes;TrustServerCertificate=no;"
    )
    return conn

@app.route('/add_product', methods=['POST'])
def add_product():
    data = request.json
    name = data['name']
    price = data['price']
    
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Products (Name, Price) VALUES (?, ?)",
            (name, price)
        )
        conn.commit()
        return jsonify({"status": "success", "id": cursor.rowcount}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn: conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)