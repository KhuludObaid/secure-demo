from flask import Flask, request
import sqlite3
import os

app = Flask(__name__)

# Hardcoded secret
SECRET_KEY = "supersecretkey123"

@app.route("/")
def home():
    return """
    <h2>Login Page</h2>
    <form action="/login" method="get">
        Username: <input name="username"><br>
        Password: <input name="password"><br>
        <input type="submit">
    </form>
    """

# SQL Injection vulnerability
@app.route("/login")
def login():
    username = request.args.get("username")
    password = request.args.get("password")

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    cursor.execute(query)  # Dangerous SQL execution

    return f"Welcome {username}"

# Reflected XSS vulnerability
@app.route("/search")
def search():
    query = request.args.get("q")
    return f"<h3>You searched for: {query}</h3>"

# Command Injection vulnerability
@app.route("/ping")
def ping():
    host = request.args.get("host")
    os.system("ping -c 1 " + host)
    return "Ping executed"

if __name__ == "__main__":
    app.run(debug=True)