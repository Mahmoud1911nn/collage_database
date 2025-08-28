import streamlit as st
import sqlite3
import pandas as pd

# الاتصال بقاعدة البيانات
conn = sqlite3.connect("collage.db")
cursor = conn.cursor()

# إنشاء الجداول
cursor.executescript("""
CREATE TABLE Students (
    StudentID INTEGER PRIMARY KEY AUTOINCREMENT,
    FullName TEXT NOT NULL,
    Age INTEGER,
    Major TEXT
);

CREATE TABLE  Professors (
    ProfessorID INTEGER PRIMARY KEY AUTOINCREMENT,
    FullName TEXT NOT NULL,
    Department TEXT
);

CREATE TABLE  Courses (
    CourseID INTEGER PRIMARY KEY AUTOINCREMENT,
    CourseName TEXT NOT NULL,
    Credits INTEGER
);

CREATE TABLE  Enrollments (
    EnrollmentID INTEGER PRIMARY KEY AUTOINCREMENT,
    StudentID INTEGER,
    CourseID INTEGER,
    Grade TEXT,
    FOREIGN KEY(StudentID) REFERENCES Students(StudentID),
    FOREIGN KEY(CourseID) REFERENCES Courses(CourseID)
);
""")
conn.commit()

# دالة تعرض جدول من قاعدة البيانات
def show_table(table):
    df = pd.read_sql(f"SELECT * FROM {table}", conn)
    st.dataframe(df)

# دالة لإضافة بيانات
def add_student(name, age, major):
    cursor.execute("INSERT INTO Students (FullName, Age, Major) VALUES (?, ?, ?)", (name, age, major))
    conn.commit()

def add_professor(name, dept):
    cursor.execute("INSERT INTO Professors (FullName, Department) VALUES (?, ?)", (name, dept))
    conn.commit()

def add_course(name, credits):
    cursor.execute("INSERT INTO Courses (CourseName, Credits) VALUES (?, ?)", (name, credits))
    conn.commit()

def add_enrollment(student_id, course_id, grade):
    cursor.execute("INSERT INTO Enrollments (StudentID, CourseID, Grade) VALUES (?, ?, ?)", (student_id, course_id, grade))
    conn.commit()

# دوال التعديل
def update_record(table, column, value, record_id, id_col):
    cursor.execute(f"UPDATE {table} SET {column}=? WHERE {id_col}=?", (value, record_id))
    conn.commit()

# دوال الحذف
def delete_record(table, record_id, id_col):
    cursor.execute(f"DELETE FROM {table} WHERE {id_col}=?", (record_id,))
    conn.commit()

# واجهة Streamlit
st.sidebar.title("📚 College Database System")
menu = st.sidebar.selectbox("Select Menu", ["Students", "Professors", "Courses", "Enrollments"])

if menu == "Students":
    st.header("👨‍🎓 Students")
    show_table("Students")

    st.subheader("➕ Add Student")
    name = st.text_input("Full Name")
    age = st.number_input("Age", 18, 60)
    major = st.text_input("Major")
    if st.button("Add Student"):
        add_student(name, age, major)
        st.success("Student Added!")

    st.subheader("✏️ Update Student Major")
    sid = st.number_input("Student ID", 1)
    new_major = st.text_input("New Major")
    if st.button("Update Major"):
        update_record("Students", "Major", new_major, sid, "StudentID")
        st.success("Student Updated!")

    st.subheader("❌ Delete Student")
    sid_del = st.number_input("Student ID to Delete", 1)
    if st.button("Delete Student"):
        delete_record("Students", sid_del, "StudentID")
        st.warning("Student Deleted!")

elif menu == "Professors":
    st.header("👨‍🏫 Professors")
    show_table("Professors")

    st.subheader("➕ Add Professor")
    pname = st.text_input("Professor Name")
    dept = st.text_input("Department")
    if st.button("Add Professor"):
        add_professor(pname, dept)
        st.success("Professor Added!")

    st.subheader("✏️ Update Professor Department")
    pid = st.number_input("Professor ID", 1)
    new_dept = st.text_input("New Department")
    if st.button("Update Professor"):
        update_record("Professors", "Department", new_dept, pid, "ProfessorID")
        st.success("Professor Updated!")

    st.subheader("❌ Delete Professor")
    pid_del = st.number_input("Professor ID to Delete", 1)
    if st.button("Delete Professor"):
        delete_record("Professors", pid_del, "ProfessorID")
        st.warning("Professor Deleted!")

elif menu == "Courses":
    st.header("📘 Courses")
    show_table("Courses")

    st.subheader("➕ Add Course")
    cname = st.text_input("Course Name")
    credits = st.number_input("Credits", 1, 6)
    if st.button("Add Course"):
        add_course(cname, credits)
        st.success("Course Added!")

    st.subheader("✏️ Update Course Credits")
    cid = st.number_input("Course ID", 1)
    new_credits = st.number_input("New Credits", 1, 6)
    if st.button("Update Course"):
        update_record("Courses", "Credits", new_credits, cid, "CourseID")
        st.success("Course Updated!")

    st.subheader("❌ Delete Course")
    cid_del = st.number_input("Course ID to Delete", 1)
    if st.button("Delete Course"):
        delete_record("Courses", cid_del, "CourseID")
        st.warning("Course Deleted!")

elif menu == "Enrollments":
    st.header("📝 Enrollments")
    show_table("Enrollments")

    st.subheader("➕ Add Enrollment")
    estudent = st.number_input("Student ID")
    ecourse = st.number_input("Course ID")
    grade = st.text_input("Grade")
    if st.button("Add Enrollment"):
        add_enrollment(estudent, ecourse, grade)
        st.success("Enrollment Added!")

    st.subheader("✏️ Update Grade")
    eid = st.number_input("Enrollment ID", 1)
    new_grade = st.text_input("New Grade")
    if st.button("Update Grade"):
        update_record("Enrollments", "Grade", new_grade, eid, "EnrollmentID")
        st.success("Enrollment Updated!")

    st.subheader("❌ Delete Enrollment")
    eid_del = st.number_input("Enrollment ID to Delete", 1)
    if st.button("Delete Enrollment"):
        delete_record("Enrollments", eid_del, "EnrollmentID")
        st.warning("Enrollment Deleted!")


