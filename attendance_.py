import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date

# DB初期化
conn = sqlite3.connect("attendance.db")
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
conn.close()

# 登録処理
def add():
    if name_entry.get() == "":
        messagebox.showerror("エラー", "名前を入力してください")
        return

    conn = sqlite3.connect("attendance.db")
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO attendance (name, date, status) VALUES (?, ?, ?)",
        (name_entry.get(), date.today().isoformat(), status_var.get())
    )
    conn.commit()
    conn.close()
    show_all()

# 表示
def show_all():
    tree.delete(*tree.get_children())
    conn = sqlite3.connect("attendance.db")
    cur = conn.cursor()
    cur.execute("SELECT name, date, status FROM attendance")
    for row in cur.fetchall():
        tree.insert("", tk.END, values=row)
    conn.close()

# GUI
root = tk.Tk()
root.title("出欠管理アプリ")

tk.Label(root, text="名前").grid(row=0, column=0)
name_entry = tk.Entry(root)
name_entry.grid(row=0, column=1)

tk.Label(root, text="出欠").grid(row=1, column=0)
status_var = tk.StringVar(value="出席")
ttk.Combobox(
    root,
    textvariable=status_var,
    values=["出席", "欠席", "遅刻"],
    state="readonly"
).grid(row=1, column=1)

tk.Button(root, text="登録", command=add).grid(row=2, column=0, columnspan=2)

tree = ttk.Treeview(root, columns=("名前", "日付", "出欠"), show="headings")
for c in ("名前", "日付", "出欠"):
    tree.heading(c, text=c)
tree.grid(row=3, column=0, columnspan=2)

show_all()
root.mainloop()
