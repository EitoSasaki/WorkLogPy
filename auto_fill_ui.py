# 同じディレクトリにあるauto_fill_ui.pyを実行する
# auto_fill_ui.pyはauto_fill.pyのUIプログラムであり、
# auto_fill.pyのコマンドを呼び出すUIを提供する
# UIには、対象年月を入力するテキストフィールドと
# エクセルファイルのパスを入力する参照ボタンと
# 「自動入力」ボタンが配置されている

import subprocess
import tkinter as tk
from tkinter import messagebox, filedialog
import sys
import pathlib
from datetime import datetime

def run_auto_fill_command(date, excel_file):
    # 実行するファイルはこのスクリプトと同じディレクトリにある auto_fill.py を想定
    script_path = pathlib.Path(__file__).resolve().parent / 'auto_fill.py'
    command = [sys.executable, str(script_path), '--date', date, '--file', excel_file]
    try:
        subprocess.run(command, check=True)
        messagebox.showinfo("成功", f"勤務ログをエクセルファイルに自動入力しました。\nファイル: {excel_file}")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("エラー", f"自動入力中にエラーが発生しました。\n{e}")

def browse_file(entry):
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls;*.xlsm")])
    if file_path:
        entry.delete(0, tk.END)
        entry.insert(0, file_path)

def create_ui():
    root = tk.Tk()
    root.title("勤務ログ自動入力UI")

    tk.Label(root, text="対象年月 (YYYYMM):").pack(pady=5)
    date_entry = tk.Entry(root)
    # デフォルトで当月 (YYYYMM) を設定
    date_entry.insert(0, datetime.now().strftime('%Y%m'))
    date_entry.pack(pady=5)

    tk.Label(root, text="エクセルファイルのパス:").pack(pady=5)
    file_frame = tk.Frame(root)
    file_frame.pack(pady=5)
    file_entry = tk.Entry(file_frame, width=40)
    file_entry.pack(side=tk.LEFT, padx=5)
    browse_button = tk.Button(file_frame, text="参照", command=lambda: browse_file(file_entry))
    browse_button.pack(side=tk.LEFT)

    fill_button = tk.Button(root, text="自動入力", command=lambda: run_auto_fill_command(date_entry.get(), file_entry.get()))
    fill_button.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    create_ui()