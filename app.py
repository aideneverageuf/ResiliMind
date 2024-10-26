from flask import Flask, render_template, request, redirect, url_for
import psycopg2

app = Flask(__name__)

# Function to connect to PostgreSQL
def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",      # Use your PostgreSQL server address
        database="resiliminddb", # Your PostgreSQL database name
        user="aiden",         # Your PostgreSQL user
        password="aiden1845"   # Your PostgreSQL user's password
    )
    return conn

# Route to display users from the database
@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM users;')  # Query to fetch all users
    users = cur.fetchall()               # Fetch all the results
    cur.close()
    conn.close()
    return render_template('index.html', users=users)  # Pass data to HTML template

# Route to insert a new user
@app.route('/add', methods=('GET', 'POST'))
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        mood = request.form['mood']

        # Insert the new user into the database
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO users (name, mood) VALUES (%s, %s)', (name, mood))
        conn.commit()
        cur.close()
        conn.close()

        return redirect(url_for('index'))  # Redirect to the main page after insertion

    return render_template('add.html')  # Display form to add a user

if __name__ == '__main__':
    app.run(debug=True)
