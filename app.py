from flask import Flask, render_template, redirect, request, url_for, flash
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from connection import connect

app = Flask(__name__)
app.secret_key = 'Likin@(2005)'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['fullname']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash("Passwords do not match!", "danger")
            return redirect(url_for('signup'))
        else:
            conn, cursor = connect() 
            query = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
            data =  (username, email, password)
            cursor.execute(query,data)
            conn.commit()
            flash("Account successfully created! Please log in.", "success")
            cursor.close()
            conn.close()
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn, cursor = connect()
        cursor.execute("SELECT password FROM users WHERE email = %s", (email,))
        data = cursor.fetchone()
        cursor.close()
        conn.close()

        if data is None:
            flash('Email not found, try again', 'danger')
            return redirect(url_for('login'))

        db_password = data[0]
        if not check_password_hash(db_password, password):
            flash('Wrong password, try again', 'danger')
            return redirect(url_for('login'))

        flash('Login successful', 'success')
        return redirect(url_for('dashboard'))

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():    
    return render_template('dashboard.html')

@app.route('/vendors')
def vendors():
    return render_template('vendors.html')

@app.route('/agenda')
def agenda():
    return render_template('agenda.html')

@app.route('/analytics')
def analytics():
    return render_template('analytics.html')

@app.route('/notification')
def notification():
    return render_template('notification.html')

@app.route('/logout')
def logout():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)