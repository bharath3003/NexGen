import mysql.connector
import streamlit as st
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
    
def login_page():
    st.title("User Login")
    name = st.text_input("Name")
    password = st.text_input("Password", type="password")
    if st.button("User_Login"):
        connection = connect_to_database()
        cursor = connection.cursor(buffered=True)

        cursor.execute("SELECT check_password(%s,%s)", (name, password))    
        result = cursor.fetchone()
        if result[0] == 1:
            st.success("Login successful.")
            st.session_state['Username'] = name
            st.title(f"Welcome, {st.session_state['Username']}")
            st.text("You can now access your profile.") 
        else:
            st.error("Invalid name or password.")
    
def sign_up():
    st.title("Sign Up")
    name = st.text_input("Name")
    password = st.text_input("Password", type="password")
    verify_password = st.text_input("Verify Password", type="password")
    
    if st.button("Sign_Up"):
        if password != verify_password:
            st.error("Passwords do not match.")
        else:
            connection = connect_to_database()
            cursor = connection.cursor(buffered=True)

            cursor.execute("SELECT check_student_name(%s)", (name,))
            result = cursor.fetchone()
            if result[0] == 1:
                st.error("Name already exists.")
            else:
                cursor.execute("SELECT add_student(%s, %s)", (name, password))
                connection.commit()
                st.success("Sign up successful. Please log in.")
    
def Login_and_signup():
    st.title("Login and Signup")
    if 'Username' not in st.session_state:
        st.session_state['Username'] = ""

    User1 = st.session_state['Username']

    if User1:
        st.text('You have already logged in as ' + User1 + ' you can go back to your profile')

    else:
        choice = st.radio("Choose an option:", ("Login", "Signup"))
        if choice == "Login":
            login_page()
        elif choice == "Signup":
            sign_up()

Login_and_signup()
