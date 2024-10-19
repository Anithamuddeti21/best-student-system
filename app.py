from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

# Database setup
DATABASE = 'student_database10.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            gpa REAL NOT NULL CHECK(gpa >= 1 AND gpa <= 100),
            hackathons_participated INTEGER DEFAULT 0,
            papers_presented INTEGER DEFAULT 0,
            teaching_assistance INTEGER DEFAULT 0,
            extracurricular_involvement INTEGER DEFAULT 0,
            final_rank_score REAL
        )
    """)
    conn.commit()
    conn.close()

def calculate_final_rank_score(row):
    weights = {
        'gpa': 0.4,
        'hackathons_participated': 0.2,
        'papers_presented': 0.15,
        'teaching_assistance': 0.1,
        'extracurricular_involvement': 0.15
    }
    return (row['gpa'] * weights['gpa'] +
            row['hackathons_participated'] * weights['hackathons_participated'] +
            row['papers_presented'] * weights['papers_presented'] +
            row['teaching_assistance'] * weights['teaching_assistance'] +
            row['extracurricular_involvement'] * weights['extracurricular_involvement'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/top_performers')
def top_performers():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute("SELECT name, final_rank_score FROM students ORDER BY final_rank_score DESC LIMIT 3")
    top_students = cursor.fetchall()
    
    conn.close()
    
    return render_template('top_performers.html', top_students=top_students)

@app.route('/view_students')
def view_students():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    
    conn.close()
    
    return render_template('view_students.html', students=students)

if __name__ == '__main__':
    init_db()  # Initialize the database
    app.run(debug=True)
