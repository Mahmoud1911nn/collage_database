# -*- coding: utf-8 -*-
import sqlite3
import pandas as pd
import streamlit as st

# إنشاء قاعدة بيانات داخل الذاكرة
conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

# جدول الطلاب
cursor.execute("""
CREATE TABLE Students (
    StudentID INTEGER PRIMARY KEY AUTOINCREMENT,
    FullName TEXT NOT NULL,
    Department TEXT,
    Email TEXT,
    EnrollmentYear INTEGER
);
""")

# جدول المقررات
cursor.execute("""
CREATE TABLE Courses (
    CourseID INTEGER PRIMARY KEY AUTOINCREMENT,
    CourseName TEXT NOT NULL,
    Credits INTEGER,
    Department TEXT
);
""")

# جدول الأساتذة
cursor.execute("""
CREATE TABLE Professors (
    ProfessorID INTEGER PRIMARY KEY AUTOINCREMENT,
    FullName TEXT NOT NULL,
    Department TEXT,
    Email TEXT
);
""")

# جدول تسجيل المقررات
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

# إدخال بيانات تجريبية
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

# ---------------------------
# واجهة Streamlit
# ---------------------------
st.title("📚 College Database System")

st.header("👨‍🎓 Students")
df_students = pd.read_sql("SELECT * FROM Students", conn)
st.dataframe(df_students)

st.header("📘 Courses")
df_courses = pd.read_sql("SELECT * FROM Courses", conn)
st.dataframe(df_courses)

st.header("👩‍🏫 Professors")
df_professors = pd.read_sql("SELECT * FROM Professors", conn)
st.dataframe(df_professors)

st.header("📝 Enrollments")
query = """
SELECT
    E.EnrollmentID, S.FullName AS StudentName, C.CourseName, E.Grade
FROM
    Enrollments E
JOIN Students S ON E.StudentID = S.StudentID
JOIN Courses C ON E.CourseID = C.CourseID;
"""
df_enrollments = pd.read_sql(query, conn)
st.dataframe(df_enrollments)
