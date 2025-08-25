# -*- coding: utf-8 -*-
import streamlit as st
import sqlite3
import pandas as pd

# إنشاء قاعدة البيانات داخل الذاكرة
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

conn.commit()

st.title("📚 College Database System")

# --- Sidebar Menu ---
menu = ["View Data", "Add Student", "Add Professor", "Add Course", "Add Enrollment"]
choice = st.sidebar.selectbox("Select Menu", menu)

if choice == "View Data":
    st.header("👨‍🎓 Students")
    st.dataframe(pd.read_sql("SELECT * FROM Students", conn))
    
    st.header("📘 Courses")
    st.dataframe(pd.read_sql("SELECT * FROM Courses", conn))
    
    st.header("👨‍🏫 Professors")
    st.dataframe(pd.read_sql("SELECT * FROM Professors", conn))
    
    st.header("📝 Enrollments")
    query = """
    SELECT E.EnrollmentID, S.FullName AS StudentName, C.CourseName, E.Grade
    FROM Enrollments E
    JOIN Students S ON E.StudentID = S.StudentID
    JOIN Courses C ON E.CourseID = C.CourseID;
    """
    st.dataframe(pd.read_sql(query, conn))

elif choice == "Add Student":
    st.header("Add New Student")
    fullname = st.text_input("Full Name")
    department = st.text_input("Department")
    email = st.text_input("Email")
    year = st.number_input("Enrollment Year", min_value=2000, max_value=2030, step=1)
    if st.button("Add Student"):
        cursor.execute("INSERT INTO Students (FullName, Department, Email, EnrollmentYear) VALUES (?, ?, ?, ?)",
                       (fullname, department, email, year))
        conn.commit()
        st.success(f"Student '{fullname}' added successfully!")

elif choice == "Add Professor":
    st.header("Add New Professor")
    fullname = st.text_input("Full Name")
    department = st.text_input("Department")
    email = st.text_input("Email")
    if st.button("Add Professor"):
        cursor.execute("INSERT INTO Professors (FullName, Department, Email) VALUES (?, ?, ?)",
                       (fullname, department, email))
        conn.commit()
        st.success(f"Professor '{fullname}' added successfully!")

elif choice == "Add Course":
    st.header("Add New Course")
    coursename = st.text_input("Course Name")
    credits = st.number_input("Credits", min_value=1, max_value=10, step=1)
    department = st.text_input("Department")
    if st.button("Add Course"):
        cursor.execute("INSERT INTO Courses (CourseName, Credits, Department) VALUES (?, ?, ?)",
                       (coursename, credits, department))
        conn.commit()
        st.success(f"Course '{coursename}' added successfully!")

elif choice == "Add Enrollment":
    st.header("Add New Enrollment")
    student_id = st.number_input("Student ID", min_value=1, step=1)
    course_id = st.number_input("Course ID", min_value=1, step=1)
    grade = st.text_input("Grade")
    
    if st.button("Add Enrollment"):
        # التحقق من وجود الطالب والمقرر
        student_exists = cursor.execute("SELECT 1 FROM Students WHERE StudentID=?", (student_id,)).fetchone()
        course_exists = cursor.execute("SELECT 1 FROM Courses WHERE CourseID=?", (course_id,)).fetchone()
        if student_exists and course_exists:
            cursor.execute("INSERT INTO Enrollments (StudentID, CourseID, Grade) VALUES (?, ?, ?)",
                           (student_id, course_id, grade))
            conn.commit()
            st.success("Enrollment added successfully!")
        else:
            st.error("StudentID or CourseID does not exist!")
