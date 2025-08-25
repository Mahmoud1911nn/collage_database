# -*- coding: utf-8 -*-
import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="📚 College Database System", layout="wide")
st.title("📚 College Database System")

# --- إنشاء قاعدة البيانات داخل الذاكرة ---
conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

# --- إنشاء الجداول ---
cursor.execute("""
CREATE TABLE Students (
    StudentID INTEGER PRIMARY KEY AUTOINCREMENT,
    FullName TEXT NOT NULL,
    Department TEXT,
    Email TEXT,
    EnrollmentYear INTEGER
);
""")

cursor.execute("""
CREATE TABLE Courses (
    CourseID INTEGER PRIMARY KEY AUTOINCREMENT,
    CourseName TEXT NOT NULL,
    Credits INTEGER,
    Department TEXT
);
""")

cursor.execute("""
CREATE TABLE Professors (
    ProfessorID INTEGER PRIMARY KEY AUTOINCREMENT,
    FullName TEXT NOT NULL,
    Department TEXT,
    Email TEXT
);
""")

cursor.execute("""
CREATE TABLE Enrollments (
    EnrollmentID INTEGER PRIMARY KEY AUTOINCREMENT,
    StudentID INTEGER,
    CourseID INTEGER,
    Grade TEXT,
    FOREIGN KEY (StudentID) REFERENCES Students(StudentID),
    FOREIGN KEY (CourseID) REFERENCES Courses(CourseID)
);
""")

# --- بيانات تجريبية ---
cursor.executemany("""
INSERT INTO Students (FullName, Department, Email, EnrollmentYear)
VALUES (?, ?, ?, ?)
""", [
    ("Ahmed Ali", "Computer Science", "ahmed.cs@example.com", 2022),
    ("Mona Hassan", "Business", "mona.bus@example.com", 2021),
    ("Omar Youssef", "Engineering", "omar.eng@example.com", 2023)
])

cursor.executemany("""
INSERT INTO Courses (CourseName, Credits, Department)
VALUES (?, ?, ?)
""", [
    ("Database Systems", 3, "Computer Science"),
    ("Marketing 101", 2, "Business"),
    ("Thermodynamics", 4, "Engineering")
])

cursor.executemany("""
INSERT INTO Professors (FullName, Department, Email)
VALUES (?, ?, ?)
""", [
    ("Dr. Samir Fahmy", "Computer Science", "samir.cs@example.com"),
    ("Dr. Hala Ibrahim", "Business", "hala.bus@example.com"),
    ("Dr. Mahmoud Tarek", "Engineering", "mahmoud.eng@example.com")
])

cursor.executemany("""
INSERT INTO Enrollments (StudentID, CourseID, Grade)
VALUES (?, ?, ?)
""", [
    (1, 1, "A"),
    (2, 2, "B+"),
    (3, 3, "A-"),
    (1, 2, "B")
])

conn.commit()

# --- واجهة إضافة بيانات ---
st.sidebar.header("➕ Add Data")

option = st.sidebar.selectbox("Choose table to add", ["Student", "Professor", "Course"])

if option == "Student":
    name = st.sidebar.text_input("Full Name")
    dept = st.sidebar.text_input("Department")
    email = st.sidebar.text_input("Email")
    year = st.sidebar.number_input("Enrollment Year", 2000, 2030, 2023)
    if st.sidebar.button("Add Student"):
        cursor.execute("INSERT INTO Students (FullName, Department, Email, EnrollmentYear) VALUES (?, ?, ?, ?)",
                       (name, dept, email, year))
        conn.commit()
        st.success(f"Student '{name}' added!")

elif option == "Professor":
    name = st.sidebar.text_input("Full Name")
    dept = st.sidebar.text_input("Department")
    email = st.sidebar.text_input("Email")
    if st.sidebar.button("Add Professor"):
        cursor.execute("INSERT INTO Professors (FullName, Department, Email) VALUES (?, ?, ?)",
                       (name, dept, email))
        conn.commit()
        st.success(f"Professor '{name}' added!")

elif option == "Course":
    cname = st.sidebar.text_input("Course Name")
    credits = st.sidebar.number_input("Credits", 1, 10, 3)
    dept = st.sidebar.text_input("Department")
    if st.sidebar.button("Add Course"):
        cursor.execute("INSERT INTO Courses (CourseName, Credits, Department) VALUES (?, ?, ?)",
                       (cname, credits, dept))
        conn.commit()
        st.success(f"Course '{cname}' added!")

# --- عرض البيانات ---
df_students = pd.read_sql("SELECT * FROM Students", conn)
df_courses = pd.read_sql("SELECT * FROM Courses", conn)
df_professors = pd.read_sql("SELECT * FROM Professors", conn)
df_enrollments = pd.read_sql("""
SELECT E.EnrollmentID, S.FullName AS StudentName, C.CourseName, E.Grade
FROM Enrollments E
JOIN Students S ON E.StudentID = S.StudentID
JOIN Courses C ON E.CourseID = C.CourseID
""", conn)

st.subheader("👨‍🎓 Students")
st.dataframe(df_students)

st.subheader("📘 Courses")
st.dataframe(df_courses)

st.subheader("👨‍🏫 Professors")
st.dataframe(df_professors)

st.subheader("📝 Enrollments")
st.dataframe(df_enrollments)

# --- تسجيل الطلاب في المقررات ---
st.sidebar.header("📝 Enroll Students")
enroll_student = st.sidebar.selectbox("Select Student", df_students["FullName"])
enroll_course = st.sidebar.selectbox("Select Course", df_courses["CourseName"])
grade = st.sidebar.text_input("Grade (مثال: A, B+, C-)")

if st.sidebar.button("Enroll Student"):
    student_id = cursor.execute("SELECT StudentID FROM Students WHERE FullName=?", (enroll_student,)).fetchone()[0]
    course_id = cursor.execute("SELECT CourseID FROM Courses WHERE CourseName=?", (enroll_course,)).fetchone()[0]
    cursor.execute("INSERT INTO Enrollments (StudentID, CourseID, Grade) VALUES (?, ?, ?)", (student_id, course_id, grade))
    conn.commit()
    st.success(f"Student '{enroll_student}' enrolled in '{enroll_course}' with grade '{grade}'!")
