from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Initialize DB
def init_db():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    # Users
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            email TEXT UNIQUE,
            password TEXT
        )
    ''')
    # Students with status
    c.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT,
            course TEXT,
            previous_course TEXT,
            contact_no TEXT,
            address TEXT,
            puc_marks TEXT,
            dob TEXT,
            submitted_by TEXT,
            status TEXT DEFAULT 'Pending'
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (name, phone, email, password) VALUES (?, ?, ?, ?)",
                      (name, phone, email, password))
            conn.commit()
            return redirect('/login')
        except sqlite3.IntegrityError:
            return "Email already registered!"
        finally:
            conn.close()
    return render_template('register.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
        user = c.fetchone()
        conn.close()

        if user:
            session['email'] = user[3]
            return redirect('/')
        else:
            return "Invalid credentials!"
    return render_template('login.html')

# Logout route
@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect('/')

# Home & form route
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'email' not in session:
            return redirect('/login')

        data = (
            request.form['student_name'],
            request.form['course'],
            request.form['previous_course'],
            request.form['contact_no'],
            request.form['address'],
            request.form['puc_marks'],
            request.form['dob'],
            #request.form['goal'],
            session['email']
        )

        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO students 
            (student_name, course, previous_course, contact_no, address, puc_marks, dob, submitted_by)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', data)
        conn.commit()
        conn.close()
        #user_email = session['user']
        
        return "submitted"
        
    if 'email' in session:
        user_email = session['email']
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        
        c.execute("SELECT name, phone FROM users WHERE email = ?", (user_email,))
        user_info = c.fetchone()
        
        c.execute("SELECT status FROM students WHERE submitted_by = ?", (user_email,))
        form_info = c.fetchone()
        
        conn.close()
        
        status = form_info[0] if form_info else 'Not Submitted'
        print("okk")
        
        return render_template('home.html', user=user_info, status=status)    
        

    return render_template('home.html')
    
# Admin login
@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        admin_id = request.form['admin_id']
        password = request.form['password']
        if admin_id == '1011' and password == '1012':
            session['admin'] = True
            return redirect('/admin')
        else:
            return "Invalid Admin Credentials"
    return render_template('admin-login.html')

# Admin dashboard
@app.route('/admin')
def admin():
    if 'admin' not in session:
        return redirect('/admin-login')
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    users = c.fetchall()
    c.execute("SELECT * FROM students")
    students = c.fetchall()
    conn.close()
    return render_template('admin.html', users=users, students=students)

# Update status route
@app.route('/update-status/<int:student_id>/<status>')
def update_status(student_id, status):
    if 'admin' not in session:
        return redirect('/admin-login')
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("UPDATE students SET status = ? WHERE id = ?", (status, student_id))
    conn.commit()
    conn.close()
    return redirect('/admin')
    
@app.route('/aboutus')
def about_us():
    if 'email' in session:
        user_email = session['email']
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        
        c.execute("SELECT name, phone FROM users WHERE email = ?", (user_email,))
        user_info = c.fetchone()
        
        c.execute("SELECT status FROM students WHERE submitted_by = ?", (user_email,))
        form_info = c.fetchone()
        
        conn.close()
        
        status = form_info[0] if form_info else 'Not Submitted'
        print("okk")
        
        return render_template('aboutus.html', user=user_info, status=status)    
    return render_template('aboutus.html')

@app.route('/facilities')
def facilities():
    if 'email' in session:
        user_email = session['email']
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        
        c.execute("SELECT name, phone FROM users WHERE email = ?", (user_email,))
        user_info = c.fetchone()
        
        c.execute("SELECT status FROM students WHERE submitted_by = ?", (user_email,))
        form_info = c.fetchone()
        
        conn.close()
        
        status = form_info[0] if form_info else 'Not Submitted'
        print("okk")
        
        return render_template('facilities.html', user=user_info, status=status)
    return render_template('facilities.html')

@app.route('/faculty')
def faculty():
    if 'email' in session:
        user_email = session['email']
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        
        c.execute("SELECT name, phone FROM users WHERE email = ?", (user_email,))
        user_info = c.fetchone()
        
        c.execute("SELECT status FROM students WHERE submitted_by = ?", (user_email,))
        form_info = c.fetchone()
        
        conn.close()
        
        status = form_info[0] if form_info else 'Not Submitted'
        print("okk")
        
        return render_template('faculty.html', user=user_info, status=status)
    return render_template('faculty.html')      
       
if __name__ == "__main__":
    app.run(debug=True)    