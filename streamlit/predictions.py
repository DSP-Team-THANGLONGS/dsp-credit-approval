import streamlit as st
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="mydatabase",
    user="myusername",
    password="mypassword"
)

def fetch_table(table_name):
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {table_name}")
    rows = cur.fetchall()
    return rows

def app():
    st.title("Table Viewer")
    
    table_name = st.text_input("Past predictions:")
    
    if table_name:
        rows = fetch_table(table_name)
        if rows:
            st.table(rows)
        else:
            st.write("No rows found.")
