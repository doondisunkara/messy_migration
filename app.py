from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import json

app = Flask(__name__)

conn = sqlite3.connect('users.db', check_same_thread=False)
cursor = conn.cursor()

def field_validation(field, field_name):
    if not field:
        return f"Require {field_name}"
    field = field.strip()
    if field == "":
        return f"Invalid User {field_name}"
    return None

@app.route('/')
def home():
    return "User Management System"

@app.route('/users', methods=['GET'])
def get_all_users():
    try:
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        return jsonify({"status": "success", "status_code": 200, "users_list": users})
    except Exception as e:
        return jsonify({"status": "error", "status_code": 500, "message": str(e)})

@app.route('/user/<user_id>', methods=['GET'])
def get_user(user_id):
    try:
        query = "SELECT * FROM users WHERE id = ?"
        cursor.execute(query, (user_id,))
        user = cursor.fetchone()
        
        if user:
            return jsonify({"status": "success", "status_code": 200, "user_details": user})
        return jsonify({"status": "failed", "status_code": 404, "message": "User Not Found"})
    except Exception as e:
        return jsonify({"status": "error", "status_code": 500, "message": str(e)})

@app.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json(force=True)
        
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')

        name_error = field_validation(name, "User Name")
        if name_error:
            return jsonify({"status": "failed", "status_code": 422, "message": name_error})

        email_error = field_validation(email, "Email")
        if email_error:
            return jsonify({"status": "failed", "status_code": 422, "message": email_error})

        password_error = field_validation(password, "Password")   
        if password_error:
            return jsonify({"status": "failed", "status_code": 422, "message": password_error})


        cursor.execute("SELECT email FROM users")
        emails_list = cursor.fetchall()
        is_email_present = any(user_email == email.lower() for user_email in emails_list)

        if is_email_present:
            return jsonify({"status": "failed", "status_code": 409, "message": "Email already found, Enter another email"})

        hash_password = generate_password_hash(password)    
        cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email.lower(), hash_password))
        conn.commit()
        
        print("User created successfully!")
        return jsonify({"status": "success", "status_code": 201, "message": "User created"})
    except Exception as e:
        return jsonify({"status": "error", "status_code": 500, "message": str(e)})

@app.route('/user/<user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        data = request.get_json(force=True)
        
        name = data.get('name')
        email = data.get('email')

        query = "SELECT * FROM users WHERE id = ?"
        cursor.execute(query, (user_id,))
        user = cursor.fetchone()
        
        if not user:
            return jsonify({"status": "failed", "status_code": 404, "message": "Invalid User ID"})
        
        if name and email:
            name = name.strip()
            if name == "":
                return jsonify({"status": "failed", "status_code": 422, "message": "Invalid User Name"})
            email = email.strip()
            if email == "":
                return jsonify({"status": "failed", "status_code": 422, "message": "Invalid User Email"})
            
            cursor.execute("SELECT * FROM users WHERE email = ? AND id != ?", (email, user_id))
            if (cursor.fetchone()):
                return jsonify({"status": "failed", "status_code": 409, "message": "Email already found, Enter another email"})
            
            cursor.execute("UPDATE users SET name = ?, email = ? WHERE id = ?", (name, email, user_id))
            conn.commit()
            return jsonify({"status": "success", "status_code": 200, "message": "User updated"})
        return jsonify({"status": "failed", "status_code": 400, "message": "Require User Data"})
    except Exception as e:
        return jsonify({"status": "error", "status_code": 500, "message": str(e)})

@app.route('/user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        query = "SELECT * FROM users WHERE id = ?"
        cursor.execute(query, (user_id,))
        user = cursor.fetchone()
        
        if not user:
            return jsonify({"status": "failed", "status_code": 404, "message": "User Id Not Found"})

        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        
        print(f"User {user_id} deleted")
        return jsonify({"status": "success", "status_code": 200, "message": "User deleted"})
    except Exception as e:
        return jsonify({"status": "error", "status_code": 500, "message": str(e)})

@app.route('/search', methods=['GET'])
def search_users():
    try:
        name = request.args.get('name')
        
        if not name:
            return {"status": "failed", "status-code": 400, "message": "Please provide a name to search"}
        
        cursor.execute("SELECT * FROM users WHERE name LIKE ?", ('%' + name + '%',))
        users = cursor.fetchall()
        return {"status": "success", "status-code": 200, "users_list": users}
    except Exception as e:
        return jsonify({"status": "error", "status_code": 500, "message": str(e)})

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json(force=True)
        email = data.get('email')
        password = data.get('password')

        email_error = field_validation(email, "Email")
        if email_error:
            return jsonify({"status": "failed", "status_code": 422, "message": email_error})

        password_error = field_validation(password, "Password")   
        if password_error:
            return jsonify({"status": "failed", "status_code": 422, "message": password_error})
        
        cursor.execute("SELECT * FROM users WHERE email = ?", (email.lower(),))
        user = cursor.fetchone()
        
        if user and check_password_hash(user[3], password):
            return jsonify({"status": "success", "status_code": 200, "user_id": user[0]})
        return jsonify({"status": "failed", "status_code": 404, "message": "Invalid Email or Password"})
    except Exception as e:
        return jsonify({"status": "error", "status_code": 500, "message": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5009, debug=True)