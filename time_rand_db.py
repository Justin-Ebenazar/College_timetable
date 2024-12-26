import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('school.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''CREATE TABLE IF NOT EXISTS teachers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS subjects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS teacher_subject (
                    teacher_id INTEGER,
                    subject_id INTEGER,
                    FOREIGN KEY(teacher_id) REFERENCES teachers(id),
                    FOREIGN KEY(subject_id) REFERENCES subjects(id),
                    PRIMARY KEY(teacher_id, subject_id))''')

conn.commit()

def options():
    opts = "addteacher assignsub dropsub dropteacher viewteacher viewteachsub".split()
    # Display available options
    while True:
        for i in opts:
            print(i, " ", opts.index(i)+1)

        n = int(input("Choose an option: "))
        
        match n:
            case 0:
                break
            case 1:
                addteacher()
            case 2:
                assignsub()
            case 3:
                dropsub()
            case 4:
                dropteacher()
            case 5:
                viewteacher()
            case 6:
                viewteachsub()
            case _:
                print("Invalid option.")

def addteacher():
    # Add multiple teachers at once
    names = input("Enter teacher names (separated by space): ").split()
    
    for name in names:
        cursor.execute("INSERT INTO teachers (name) VALUES (?)", (name,))
        conn.commit()
        print(f"Teacher '{name}' added.")

def assignsub():
    # Assign multiple subjects to a teacher
    teacher_name = input("Enter teacher's name: ")
    subjects = input("Enter subjects (separated by space): ").split()

    # Check if teacher exists
    cursor.execute("SELECT id FROM teachers WHERE name = ?", (teacher_name,))
    teacher = cursor.fetchone()
    
    if not teacher:
        print("Teacher not found.")
        return

    teacher_id = teacher[0]

    for subject_name in subjects:
        # Check if subject exists, if not, add it
        cursor.execute("SELECT id FROM subjects WHERE name = ?", (subject_name,))
        subject = cursor.fetchone()
        
        if not subject:
            cursor.execute("INSERT INTO subjects (name) VALUES (?)", (subject_name,))
            conn.commit()
            cursor.execute("SELECT id FROM subjects WHERE name = ?", (subject_name,))
            subject = cursor.fetchone()

        subject_id = subject[0]

        # Check if the teacher already has this subject
        cursor.execute("SELECT * FROM teacher_subject WHERE teacher_id = ? AND subject_id = ?", (teacher_id, subject_id))
        if cursor.fetchone():
            print(f"{teacher_name} already has {subject_name}.")
        else:
            cursor.execute("INSERT INTO teacher_subject (teacher_id, subject_id) VALUES (?, ?)", (teacher_id, subject_id))
            conn.commit()
            print(f"Assigned subject '{subject_name}' to teacher '{teacher_name}'.")

def dropsub():
    # Drop a specific subject of a teacher
    teacher_name = input("Enter teacher's name: ")
    subject_name = input("Enter subject name to drop: ")

    # Check if teacher exists
    cursor.execute("SELECT id FROM teachers WHERE name = ?", (teacher_name,))
    teacher = cursor.fetchone()
    
    if not teacher:
        print("Teacher not found.")
        return

    teacher_id = teacher[0]

    # Check if subject exists
    cursor.execute("SELECT id FROM subjects WHERE name = ?", (subject_name,))
    subject = cursor.fetchone()
    
    if not subject:
        print("Subject not found.")
        return

    subject_id = subject[0]

    # Remove subject from the teacher
    cursor.execute("DELETE FROM teacher_subject WHERE teacher_id = ? AND subject_id = ?", (teacher_id, subject_id))
    conn.commit()
    print(f"Dropped subject '{subject_name}' from teacher '{teacher_name}'.")

def dropteacher():
    # Drop a teacher and all their subjects
    teacher_name = input("Enter teacher's name to remove: ")

    cursor.execute("SELECT id FROM teachers WHERE name = ?", (teacher_name,))
    teacher = cursor.fetchone()

    if not teacher:
        print("Teacher not found.")
        return

    teacher_id = teacher[0]

    # Delete the teacher's assignments
    cursor.execute("DELETE FROM teacher_subject WHERE teacher_id = ?", (teacher_id,))
    conn.commit()

    # Delete the teacher
    cursor.execute("DELETE FROM teachers WHERE id = ?", (teacher_id,))
    conn.commit()
    print(f"Teacher '{teacher_name}' and all their subjects have been removed.")

def viewteacher():
    # View all teachers
    cursor.execute("SELECT name FROM teachers")
    teachers = cursor.fetchall()
    
    if not teachers:
        print("No teachers found.")
    else:
        print("Teachers list:")
        for teacher in teachers:
            print(teacher[0])

def viewteachsub():
    # View subjects assigned to a specific teacher
    teacher_name = input("Enter teacher's name: ")

    cursor.execute("SELECT id FROM teachers WHERE name = ?", (teacher_name,))
    teacher = cursor.fetchone()

    if not teacher:
        print("Teacher not found.")
        return

    teacher_id = teacher[0]

    # Fetch subjects for the teacher
    cursor.execute('''
        SELECT subjects.name 
        FROM subjects 
        JOIN teacher_subject ON subjects.id = teacher_subject.subject_id
        WHERE teacher_subject.teacher_id = ?
    ''', (teacher_id,))
    
    subjects = cursor.fetchall()

    if not subjects:
        print(f"{teacher_name} is not assigned any subjects.")
    else:
        print(f"Subjects handled by {teacher_name}:")
        for subject in subjects:
            print(subject[0])

# Main program
options()

# Close the connection to the database when done
conn.close()
