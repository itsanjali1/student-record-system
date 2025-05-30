from flask import Flask, request, redirect, url_for, session, flash, send_file

from werkzeug.security import check_password_hash
import mysql.connector
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.permanent_session_lifetime = timedelta(minutes=30)

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='anjali',
        database='student_record_system'
    )

# Verify user credentials
def verify_user(table, username, password):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM {table} WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    if user and check_password_hash(user['password'], password):
        return True
    return False

@app.route('/')
def main_login():
    return redirect(url_for('admin_login'))  # Or create a main login page if you want

# Admin Login
@app.route('/admin_login')
def admin_login():
    return app.send_static_file('admin_login.html')

@app.route('/admin_dashboard', methods=['POST'])
def admin_dashboard():
    username = request.form['username']
    password = request.form['password']

    if verify_user('admin', username, password):
        session.permanent = True
        session['role'] = 'admin'
        session['username'] = username
        return redirect('/static/admin_dashboard.html')  # Static HTML page
    else:
        return redirect('/admin_login?error=Invalid+credentials')

# Faculty Login
@app.route('/faculty_login')
def faculty_login():
    return app.send_static_file('faculty_login.html')

@app.route('/faculty_dashboard', methods=['POST'])
def faculty_dashboard():
    username = request.form['username']
    password = request.form['password']

    if verify_user('faculty', username, password):
        session.permanent = True
        session['role'] = 'faculty'
        session['username'] = username
        return redirect('/static/faculty_dashboard.html')
    else:
        return redirect('/faculty_login?error=Invalid+credentials')

# Student Login
@app.route('/student_login')
def student_login():
    return app.send_static_file('student_login.html')

@app.route('/student_dashboard', methods=['POST'])
def student_dashboard():
    username = request.form['username']
    password = request.form['password']

    if verify_user('student', username, password):
        session.permanent = True
        session['role'] = 'student'
        session['username'] = username
        return redirect('/static/student_dashboard.html')
    else:
        return redirect('/student_login?error=Invalid+credentials')

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
