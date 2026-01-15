import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date

# ---------- データベース初期化 ----------
def init_db():
    conn = sqlite3.connect("attendance.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            date TEXT NOT NULL,
            status TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# ---------- 出欠登録 ----------
def add_attendance():
    name = name_entry.get()
    status = status_var.get()
    today = date.today().isoformat()

    if name == "":
        messagebox.showerror("エラー", "名前を入力してください")
        return

    conn = sqlite3.connect("attendance.db")
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO attendance (name, date, status) VALUES (?, ?, ?)",
        (name, today, status)
    )
    conn.commit()
    conn.close()

    name_entry.delete(0, tk.END)
    load_all()

# ---------- 一覧表示 ----------
def load_all():
    for row in tree.get_children():
        tree.delete(row)

    conn = sqlite3.connect("attendance.db")
    cur = conn.cursor()
    cur.execute("SELECT name, date, status FROM attendance")
    rows = cur.fetchall()
    conn.close()

    for row in rows:
        tree.insert("", tk.END, values=row)

# ---------- 欠席者のみ表示（独自改良） ----------
def load_absent():
    for row in tree.get_children():
        tree.delete(row)

    conn = sqlite3.connect("attendance.db")
    cur = conn.cursor()
    cur.execute("SELECT name, date, status FROM attendance WHERE status='欠席'")
    rows = cur.fetchall()
    conn.close()

    for row in rows:
        tree.insert("", tk.END, values=row)

# ---------- 出席率表示（独自改良） ----------
def show_rate():
    conn = sqlite3.connect("attendance.db")
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM attendance")
    total = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM attendance WHERE status='出席'")
    present = cur.fetchone()[0]

    conn.close()

    if total == 0:
        rate = 0
    else:
        rate = (present / total) * 100

    messagebox.showinfo("出席率", f"出席率：{rate:.1f}%")

# ---------- GUI ----------
init_db()

root = tk.Tk()
root.title("出欠管理アプリ")

tk.Label(root, text="名前").grid(row=0, column=0, padx=5, pady=5)
name_entry = tk.Entry(root)
name_entry.grid(row=0, column=1)

tk.Label(root, text="出欠").grid(row=1, column=0, padx=5)
status_var = tk.StringVar()
status_box = ttk.Combobox(
    root,
    textvariable=status_var,
    values=["出席", "欠席", "遅刻"],
    state="readonly"
)
status_box.current(0)
status_box.grid(row=1, column=1)

tk.Button(root, text="登録", command=add_attendance).grid(row=2, column=0, columnspan=2, pady=5)

columns = ("名前", "日付", "出欠")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
tree.grid(row=3, column=0, columnspan=2, pady=10)

tk.Button(root, text="全件表示", command=load_all).grid(row=4, column=0)
tk.Button(root, text="欠席のみ表示", command=load_absent).grid(row=4, column=1)
tk.Button(root, text="出席率表示", command=show_rate).grid(row=5, column=0, columnspan=2, pady=5)

load_all()
root.mainloop()
