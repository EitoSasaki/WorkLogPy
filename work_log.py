# 勤務時間を記録し、jsonファイルに保存するプログラム
# ユーザーが勤務開始か終了の時間を入力し、そのデータをjson形式で保存する
# 開始と終了はコマンドライン引数で、どちらか一方だけ記録可能
# --startで勤務開始時間を現在時刻で記録
# --endで勤務終了時間を現在時刻で記録
# --break_timeで休憩時間を現在時刻で記録
# 例: python work_log.py --start
# コマンドライン引数が設定されているもののみを記録する
# 既に同じ日のデータが存在する場合は、上書き保存する
# 保存先のjsonファイルは "YYYYMM_work_log.json"
# jsonの形式は以下の通り
# {
#     "YYYY-MM-DD": [
#         {
#             "start": "HH:MM",
#             "end": "HH:MM",
#             "break_time": "HH:MM"
#         }
#     ],
#     ...
# }

import json
import os
import argparse
from datetime import datetime
import sys
import pathlib

def load_work_log(file_path):
    # 既存の勤務ログを読み込む
    # 既存のファイルが存在しなければ新規ファイルを作成
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            json.dump({}, f)
    with open(file_path, 'r') as f:
        return json.load(f)
    
def save_work_log(file_path, data):
    # 勤務ログを保存する
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

def record_time(log, date_str, time_type, time_str):
    # 指定された日にちの勤務時間を記録する
    if date_str not in log:
        log[date_str] = [{}]
    if time_type not in log[date_str][0]:
        log[date_str][0][time_type] = time_str
    else:
        log[date_str][0][time_type] = time_str  # 上書き保存
    return log

def main():
    parser = argparse.ArgumentParser(description="勤務時間を記録するプログラム")
    parser.add_argument('--start', action='store_true', help='勤務開始時間を記録')
    parser.add_argument('--end', action='store_true', help='勤務終了時間を記録')
    parser.add_argument('--break_time', action='store_true', help='休憩時間を記録')
    args = parser.parse_args()

    if not (args.start or args.end or args.break_time):
        print("エラー: --start, --end, または --break_time のいずれかを指定してください。")
        sys.exit(1)

    # 保存先はこのスクリプトがあるディレクトリの output フォルダ内の YYYYMM_work_log.json
    script_dir = pathlib.Path(__file__).resolve().parent
    output_dir = script_dir / 'output'
    output_dir.mkdir(parents=True, exist_ok=True)
    now = datetime.now()
    filename = f"{now.strftime('%Y%m')}_work_log.json"
    file_path = output_dir / filename
    work_log = load_work_log(file_path)

    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M")

    if args.start:
        work_log = record_time(work_log, date_str, 'start', time_str)
    if args.end:
        work_log = record_time(work_log, date_str, 'end', time_str)
    if args.break_time:
        work_log = record_time(work_log, date_str, 'break_time', time_str)

    save_work_log(file_path, work_log)
    print(f"勤務時間が記録されました: {file_path}")

if __name__ == "__main__":
    main()