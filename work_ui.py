# work_log.pyのコマンドを呼び出すUIプログラム
# 呼び出すコマンドは--start, --end, --break_timeのいずれか
# それぞれのコマンドをボタンで実行できるようにする

import subprocess
import tkinter as tk
from tkinter import messagebox
import sys
import pathlib
from datetime import datetime

def run_work_log_command(arg, label=None):
    # 実行するファイルはこのスクリプトと同じディレクトリにある work_log.py を想定
    script_path = pathlib.Path(__file__).resolve().parent / 'work_log.py'
    command = [sys.executable, str(script_path), arg]
    try:
        subprocess.run(command, check=True)
        # 成功したら実行したコマンドと現在時刻を表示
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # ボタン名が指定されていればそれを表示、なければ引数を表示
        display = label if label else arg
        messagebox.showinfo(f"{display}", f"記録しました。\n実行時刻: {now}")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("エラー", f"{label or arg} コマンドの実行中にエラーが発生しました。\n{e}")

def create_ui():
    root = tk.Tk()
    root.title("勤務時間記録UI")

    start_button = tk.Button(root, text="勤務開始", command=lambda: run_work_log_command('--start', '勤務開始'))
    start_button.pack(pady=10)

    end_button = tk.Button(root, text="勤務終了", command=lambda: run_work_log_command('--end', '勤務終了'))
    end_button.pack(pady=10)

    break_button = tk.Button(root, text="休憩", command=lambda: run_work_log_command('--break_time', '休憩'))
    break_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_ui()