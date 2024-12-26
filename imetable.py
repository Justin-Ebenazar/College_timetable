import sqlite3
import random
conn = sqlite3.connect('school.db')
cursor = conn.cursor()
def create_database():
    global cursor
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS teachers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS classes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS teacher_subject (
            teacher_id INTEGER,
            subject_id INTEGER,
            class_id INTEGER,
            FOREIGN KEY(teacher_id) REFERENCES teachers(id),
            FOREIGN KEY(subject_id) REFERENCES subjects(id),
            FOREIGN KEY(class_id) REFERENCES classes(id),
            PRIMARY KEY(teacher_id, subject_id, class_id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS timetables (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            class_id INTEGER,
            day INTEGER,
            period INTEGER,
            subject_id INTEGER,
            teacher_id INTEGER,
            FOREIGN KEY(class_id) REFERENCES classes(id),
            FOREIGN KEY(subject_id) REFERENCES subjects(id),
            FOREIGN KEY(teacher_id) REFERENCES teachers(id)
        )
    ''')
    conn.commit()
    conn.close()
f = 1
def options():
    global f
    opts = ["addteacher", "assignsub", "dropteacher", "viewteacher", "viewteachsub", "createclass", "dropclass", "viewclasses", "generatetimetable", "truncatetimetable"]
    while True:
        if f:
            for i, opt in enumerate(opts):
                print(i+1, opt)
                f = 0
        choice = int(input("Enter your choice: "))
        if choice == 1:
            addteacher()
        elif choice == 2:
            assignsub()
        elif choice == 3:
            dropteacher()
        elif choice == 4:
            viewteacher()
        elif choice == 5:
            viewteachsub()
        elif choice == 6:
            createclass()
        elif choice == 7:
            dropclass()
        elif choice == 8:
            viewclasses()
        elif choice == 9:
            generatetimetable()
        elif choice == 10:
            truncatetimetable()
        elif choice == 11:
            showtt()
        else:
            print("Invalid option.")

def addteacher():
    name = input("Enter teacher name: ")
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO teachers (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()
    print(f"Teacher '{name}' added.")

def assignsub():
    teacher_name = input("Enter teacher's name: ")
    class_name = input("Enter class name: ")
    subjects = input("Enter subjects (separated by space): ").split()

    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM teachers WHERE name = ?", (teacher_name,))
    teacher = cursor.fetchone()
    cursor.execute("SELECT id FROM classes WHERE name = ?", (class_name,))
    class_id = cursor.fetchone()[0]

    if not teacher:
        print("Teacher not found.")
        return

    teacher_id = teacher[0]

    for subject_name in subjects:
        cursor.execute("SELECT id FROM subjects WHERE name = ?", (subject_name,))
        subject = cursor.fetchone()
        if not subject:
            cursor.execute("INSERT INTO subjects (name) VALUES (?)", (subject_name,))
            conn.commit()
            cursor.execute("SELECT id FROM subjects WHERE name = ?", (subject_name,))
            subject = cursor.fetchone()

        subject_id = subject[0]

        cursor.execute("INSERT INTO teacher_subject (teacher_id, subject_id, class_id) VALUES (?, ?, ?)", (teacher_id, subject_id, class_id))
        conn.commit()
        print(f"Assigned subject '{subject_name}' to teacher '{teacher_name}' for class '{class_name}'.")

    conn.close()

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

def createclass():
    class_name = input("Enter class name: ")
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO classes (name) VALUES (?)", (class_name,))
    conn.commit()
    conn.close()
    print(f"Class '{class_name}' added.")

def dropclass():
    class_name = input("Enter class name to drop: ")
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM classes WHERE name = ?", (class_name,))
    conn.commit()
    conn.close()
    print(f"Class '{class_name}' and its timetable have been removed.")

def viewclasses():
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM classes")
    classes = cursor.fetchall()
    if not classes:
        print("No classes found.")
    else:
        print("Classes:")
        for cls in classes:
            print(cls[0])
    conn.close()

def generatetimetable():
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()

    cursor.execute("SELECT c.id, c.name, s.name, ts.subject_id, ts.teacher_id FROM classes c JOIN teacher_subject ts ON c.id = ts.class_id JOIN subjects s ON ts.subject_id = s.id")
    class_subjects = cursor.fetchall()

    # print(class_subjects)
    # for i in class_subjects:
    #     print(i)

    timetables = {}
    for class_id, class_name, subject_name, subject_id, teacher_id in class_subjects:
        if class_name not in timetables:
            timetables[class_name] = [[None] * 8 for _ in range(6)]

        assigned = False
        while not assigned:
            day = random.randint(0, 5)
            period = random.randint(0, 7)
            if timetables[class_name][day][period] is None:
                cursor.execute("SELECT * FROM timetables WHERE teacher_id = ? AND day = ? AND period = ?", (teacher_id, day, period))
                if not cursor.fetchone():
                    timetables[class_name][day][period] = (subject_name, "teacher_id")
                    cursor.execute("INSERT INTO timetables (class_id, day, period, subject_id, teacher_id) VALUES (?, ?, ?, ?, ?)", (class_id, day, period, subject_id, teacher_id))
                    conn.commit()
                    assigned = True

    for class_name, timetable in timetables.items():
        print(f"Timetable for {class_name}:")
        for day in range(6):
            print(f"Day {day+1}:")
            for period in range(8):
                if timetable[day][period]:
                    subject, teacher = timetable[day][period]
                    # print(f"Period {period+1}: {subject} ({teacher})")
                else:
                    pass
                    # print(f"Period {period+1}: Free")
    conn.close()
def showtt():
    cursor.execute("select * from timetables")
    print(cursor.fetchall())

def truncatetimetable():
    class_name = input("Enter class name to truncate timetable: ")
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM timetables WHERE class_id = (SELECT id FROM classes WHERE name = ?)", (class_name,))
    conn.commit()
    conn.close()
    print(f"Timetable for {class_name} truncated.")
options()