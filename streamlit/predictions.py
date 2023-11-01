import streamlit as st
import psycopg2
import pandas as pd

conn = psycopg2.connect(
    host="localhost",
    database="mydatabase",
    user="myusername",
    password="mypassword"
)

cur = conn.cursor()

cur.execute("SELECT * FROM mytable")

rows = cur.fetchall()

df = pd.DataFrame(rows, columns=[desc[0] for desc in cur.description])

cur.close()
conn.close()

st.table(df)
