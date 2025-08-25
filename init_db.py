import sqlite3

# الاتصال بقاعدة البيانات (لو مش موجودة هيعملها)
conn = sqlite3.connect("collage.db")
cursor = conn.cursor()

# ----------- إنشاء الجداول -----------

# جدول الطلاب
cursor.execute("""
CREATE TABLE IF NOT EXISTS Students (
    StudentID INTEGER PRIMARY KEY AUTOINCREMENT,
    FullName TEXT NOT NULL,
    Age INTEGER,
    Major TEXT
);
""")

# جدول الأساتذة
cursor.execute("""
CREATE TABLE IF NOT EXISTS Professors (
    ProfessorID INTEGER PRIMARY KEY AUTOINCREMENT,
    FullName TEXT NOT NULL,
    Department TEXT
);
""")

# جدول الكورسات
cursor.execute("""
CREATE TABLE IF NOT EXISTS Courses (
    CourseID INTEGER PRIMARY KEY AUTOINCREMENT,
    CourseName TEXT NOT NULL,
    Credits INTEGER,
    ProfessorID INTEGER,
    FOREIGN KEY (ProfessorID) REFERENCES Professors(ProfessorID)
);
""")

# جدول التسجيلات (العلاقة بين الطلاب والكورسات)
cursor.execute("""
CREATE TABLE IF NOT EXISTS Enrollments (
    EnrollmentID INTEGER PRIMARY KEY AUTOINCREMENT,
    StudentID INTEGER,
    CourseID INTEGER,
    Grade TEXT,
    FOREIGN KEY (StudentID) REFERENCES Students(StudentID),
    FOREIGN KEY (CourseID) REFERENCES Courses(CourseID)
);
""")

# ----------- إدخال بيانات تجريبية -----------

# بيانات الطلاب
cursor.executemany("""
INSERT INTO Students (FullName, Age, Major)
VALUES (?, ?, ?)
""", [
    ("Ahmed Ali", 21, "Computer Science"),
    ("Sara Mohamed", 22, "Information Systems"),
    ("Omar Hassan", 20, "Data Science"),
    ("Mona Ibrahim", 23, "Artificial Intelligence"),
    ("Nour Ahmed", 21, "Cyber Security")
])

# بيانات الأساتذة
cursor.executemany("""
INSERT INTO Professors (FullName, Department)
VALUES (?, ?)
""", [
    ("Dr. Khaled Youssef", "Computer Science"),
    ("Dr. Salma Fathy", "Information Systems"),
    ("Dr. Hany Adel", "Artificial Intelligence")
])

# بيانات الكورسات
cursor.executemany("""
INSERT INTO Courses (CourseName, Credits, ProfessorID)
VALUES (?, ?, ?)
""", [
    ("Database Systems", 3, 1),
    ("Machine Learning", 4, 3),
    ("Cyber Security Basics", 3, 2),
    ("Data Mining", 4, 1)
])

# بيانات التسجيلات (Enrollments)
cursor.executemany("""
INSERT INTO Enrollments (StudentID, CourseID, Grade)
VALUES (?, ?, ?)
""", [
    (1, 1, "A"),
    (1, 2, "B+"),
    (2, 1, "A-"),
    (3, 3, "B"),
    (4, 2, "A"),
    (5, 4, "B+")
])

# حفظ التغييرات
conn.commit()
conn.close()

print("✅ Database created and sample data inserted successfully!")
