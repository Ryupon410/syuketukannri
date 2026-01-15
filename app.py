import streamlit as st
import sqlite3
from datetime import date

# DB接続
conn = sqlite3.connect("attendance.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    date TEXT,
    status TEXT
)
""")
conn.commit()

st.title("出欠管理アプリ")

# 入力
name = st.text_input("名前")
status = st.selectbox("出欠", ["出席", "欠席", "遅刻"])

if st.button("登録"):
    if name:
        cur.execute(
            "INSERT INTO attendance (name, date, status) VALUES (?, ?, ?)",
            (name, date.today().isoformat(), status)
        )
        conn.commit()
        st.success("登録しました")

st.divider()

# 表示切り替え
view = st.radio("表示", ["全件", "欠席のみ"])

if view == "全件":
    cur.execute("SELECT name, date, status FROM attendance")
else:
    cur.execute("SELECT name, date, status FROM attendance WHERE status='欠席'")

rows = cur.fetchall()
st.table(rows)
