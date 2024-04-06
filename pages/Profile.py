import streamlit as st
import mysql.connector
from mysql.connector import Error

def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            database="student_scores"
        )
        return connection
    except Error as e:
        st.error(f"Error: {e}")
        return None

def update_user_info(username, password, new_password=None):
    connection = connect_to_database()
    cursor = connection.cursor()

    if new_password:
        cursor.execute("UPDATE students SET password = %s WHERE name = %s", (new_password, username))
    else:
        cursor.execute("SELECT * FROM students WHERE name = %s", (username,))
        user_info = cursor.fetchone()
        st.text(f"Username: {user_info[1]}")
        st.text(f"Score: {user_info[3]}")
        st.text(f"Subject: {user_info[4]}")
        st.text(f"Easy Questions Solved: {user_info[5]}")
        st.text(f"Medium Questions Solved: {user_info[6]}")
        st.text(f"Hard Questions Solved: {user_info[7]}")

    connection.commit()

    cursor.close()
    connection.close()
    st.success("User information updated successfully.")

def ProfilePage(User1):
    st.subheader(f"Hey, {User1}, feel like changing your profile?")
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM students WHERE name = '{User1}'")
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    if result:
        update_user_info(User1, result[0][2])  # Update only the password by default
        new_password = st.text_input("New Password", type="password")
        if new_password:
            update_user_info(User1, result[0][2], new_password=new_password)
    else:
        st.warning("User not found.")

# Check if the user is logged in
if 'Username' not in st.session_state:
    st.session_state["Username"] = ""

User1 = st.session_state['Username']

if User1 != "":
    ProfilePage(User1)
else:
    st.warning("You need to log in to access this page.")
