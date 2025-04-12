from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'secret123'

# DB connection
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="arunatarak",
        database="institutehub"
    )

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        role = request.form['role']
        username = request.form['username']
        password = request.form['password']

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM users WHERE username = %s AND role = %s", (username, role))
        user = cursor.fetchone()
        conn.close()

        if user and user['password'] == password:
            session['username'] = user['username']
            session['role'] = user['role']
            if role == 'student':
                return redirect(url_for('student_dashboard'))
            elif role == 'faculty':
                return redirect(url_for('faculty_dashboard'))
        else:
            # Pass a message to the login page
            return render_template("login.html", message="Account does not exist. Please register first.")

    return render_template("login.html")

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    return redirect(url_for('home'))

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register_user', methods=['POST'])
def register_user():
    username = request.form['username']
    password = request.form['password']
    name=request.form['name']
    role = request.form.get('role')
    email=request.form['email']
    

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password, full_name, email, role) VALUES (%s, %s, %s, %s, %s)",(username, password, name, email, role))
    conn.commit()
    conn.close()

    flash("Registration successful. Please log in.")
    return redirect(url_for('home'))



@app.route('/create_announcement', methods=['GET', 'POST'])
def create_announcement():
    if 'username' not in session:
        return redirect(url_for('home'))
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO announcements (title, content) VALUES (%s, %s)", (title, content))
        conn.commit()
        conn.close()
        flash("Announcement posted.")
        return redirect(url_for('dashboard'))
    return render_template('create_announcement.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/student_dashboard')
def student_dashboard():
    if 'username' not in session or session['role'] != 'student':
        return redirect(url_for('home'))

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Get student info
    cursor.execute("SELECT * FROM users WHERE username=%s", (session['username'],))
    student = cursor.fetchone()
    student_id = student['id']

    # All available events
    cursor.execute("SELECT * FROM events ORDER BY date ASC")
    events = cursor.fetchall()

    # Registered events from tech, cultural, sports
    user_events = []
    registered_event_ids = []

    for cat in ['tech', 'cultural', 'sports']:
        cursor.execute(f"""
            SELECT e.* FROM {cat}_events te
            JOIN events e ON te.event_id = e.id
            WHERE te.student_id = %s
        """, (student_id,))
        reg_events = cursor.fetchall()
        user_events += reg_events
        registered_event_ids += [e['id'] for e in reg_events]

    # 📢 Announcements (posted_by name from users table)
    cursor.execute("""
        SELECT a.*, u.username AS posted_by 
        FROM announcements a
        JOIN users u ON a.posted_by = u.id
        ORDER BY a.id DESC
    """)
    announcements = cursor.fetchall()

    # ✅ All Tasks (no filter)
    cursor.execute("SELECT * FROM tasks ORDER BY id DESC")
    tasks = cursor.fetchall()

    conn.close()

    return render_template('student_dashboard.html',
                           username=session['username'],
                           events=events,
                           user_events=user_events,
                           registered_events=registered_event_ids,
                           announcements=announcements,
                           tasks=tasks)

@app.route('/faculty_dashboard')
def faculty_dashboard():
    if 'username' not in session or session['role'] != 'faculty':
        return redirect(url_for('home'))

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Get faculty ID
    cursor.execute("SELECT id FROM users WHERE username = %s", (session['username'],))
    faculty = cursor.fetchone()
    faculty_id = faculty['id']

    # Events created by this faculty
    cursor.execute("SELECT * FROM events WHERE created_by = %s ORDER BY date ASC", (faculty_id,))
    your_events = cursor.fetchall()

    # Announcements by this faculty
    cursor.execute("SELECT * FROM announcements WHERE posted_by = %s ORDER BY id DESC", (faculty_id,))
    your_announcements = cursor.fetchall()

    # Tasks created by this faculty
    cursor.execute("SELECT * FROM tasks WHERE assigned_by = %s ORDER BY id DESC", (session['username'],))
    your_tasks = cursor.fetchall()

    # No registrations loaded yet
    registrations = []
    selected_type = None

    conn.close()

    return render_template('faculty_dashboard.html',
                           username=session['username'],
                           your_events=your_events,
                           your_announcements=your_announcements,
                           your_tasks=your_tasks,
                           registrations=registrations,
                           selected_type=selected_type)


@app.route('/view_registrations')
def view_registrations():
    if 'username' not in session or session['role'] != 'faculty':
        return redirect(url_for('home'))

    selected_type = request.args.get('event_type')
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Get faculty ID
    cursor.execute("SELECT id FROM users WHERE username = %s", (session['username'],))
    faculty = cursor.fetchone()
    faculty_id = faculty['id']

    # Events created by this faculty
    cursor.execute("SELECT * FROM events WHERE created_by = %s ORDER BY date ASC", (faculty_id,))
    your_events = cursor.fetchall()

    # Announcements by this faculty
    cursor.execute("SELECT * FROM announcements WHERE posted_by = %s ORDER BY id DESC", (faculty_id,))
    your_announcements = cursor.fetchall()

    # Tasks created by this faculty
    cursor.execute("SELECT * FROM tasks WHERE assigned_by = %s ORDER BY id DESC", (session['username'],))
    your_tasks = cursor.fetchall()

    # Fetch registrations based on event type
    registrations = []
    if selected_type == "Tech":
        cursor.execute("SELECT * FROM tech_events")
        registrations = cursor.fetchall()
    elif selected_type == "Cultural":
        cursor.execute("SELECT * FROM cultural_events")
        registrations = cursor.fetchall()
    elif selected_type == "Sports":
        cursor.execute("SELECT * FROM sports_events")
        registrations = cursor.fetchall()

    conn.close()

    return render_template('faculty_dashboard.html',
                           username=session['username'],
                           your_events=your_events,
                           your_announcements=your_announcements,
                           your_tasks=your_tasks,
                           registrations=registrations,
                           selected_type=selected_type)




@app.route('/register_event/<int:event_id>', methods=['POST'])
def register_event(event_id):
    if 'username' not in session or session['role'] != 'student':
        return redirect(url_for('home'))

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Get student info
    cursor.execute("SELECT * FROM users WHERE username=%s", (session['username'],))
    student = cursor.fetchone()
    student_id = student['id']
    student_name=student['full_name']

    # Get event info
    cursor.execute("SELECT * FROM events WHERE id=%s", (event_id,))
    event = cursor.fetchone()

    category = event['category'].lower()
    reg_table = f"{category}_events"

    # Check if already registered
    cursor.execute(f"SELECT * FROM {reg_table} WHERE student_id=%s AND event_id=%s", (student_id, event_id))
    exists = cursor.fetchone()

    if not exists:
        cursor.execute(f"INSERT INTO {reg_table} (student_id, event_id,stu_name) VALUES (%s, %s,%s)", (student_id, event_id,student_name))
        conn.commit()

    conn.close()
    return redirect(url_for('student_dashboard'))

@app.route('/create_event', methods=['POST'])
def create_event():
    if 'username' not in session or session['role'] != 'faculty':
        return redirect(url_for('home'))

    # Get form data
    title = request.form['title']
    description = request.form['description']
    date = request.form['date']
    category = request.form['category']

    # First get connection and cursor
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)  # Use dictionary=True to access keys like 'id'

    # Get faculty ID from session
    cursor.execute("SELECT * FROM users WHERE username=%s", (session['username'],))
    faculty = cursor.fetchone()
    faculty_id = faculty['id']

    # Insert event
    cursor.execute("""
        INSERT INTO events (title, description, date, category, created_by)
        VALUES (%s, %s, %s, %s, %s)
    """, (title, description, date, category, faculty_id))

    conn.commit()
    conn.close()

    flash("Event created successfully!")
    return redirect(url_for('faculty_dashboard'))


@app.route('/post_announcement', methods=['POST'])
def post_announcement():
    title = request.form['title']
    content = request.form['content']
    
    # First create the connection and cursor
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)  # use dictionary=True to fetch dict-style row
    
    # Get faculty ID from session
    cursor.execute("SELECT * FROM users WHERE username=%s", (session['username'],))
    faculty = cursor.fetchone()
    faculty_id = faculty['id']

    # Now insert announcement
    cursor.execute(
        "INSERT INTO announcements (title, content, posted_by) VALUES (%s, %s, %s)",
        (title, content, faculty_id)
    )
    
    conn.commit()
    conn.close()

    flash("Announcement posted!")
    return redirect(url_for('faculty_dashboard'))


  

@app.route('/assign_task', methods=['POST'])
def assign_task():
    title = request.form['title']
    description = request.form['description']
    posted_by = session.get('username')
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (title, description,assigned_by) VALUES (%s, %s,%s)", (title, description,posted_by))
    conn.commit()
    conn.close()
    flash("Task assigned successfully!")
    return redirect(url_for('faculty_dashboard'))

@app.route('/admin_dashboard')
def admin_dashboard():
    if session.get('role') != 'admin':
        return redirect(url_for('home'))
    return render_template('admin_dashboard.html', username=session['username'])



if __name__ == '__main__':
    app.run(debug=True)
