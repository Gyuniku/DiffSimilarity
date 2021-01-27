# -*- coding: utf-8 -*-

import sys
import csv
import tkinter, tkinter.filedialog, tkinter.messagebox
import difflib
import os
import datetime

# 結果を出力するフォルダ(ファイルの実行場所)
save_dir = os.path.dirname(__file__)
# 出力ファイル名
save_filename = 'result'
# 出力ファイルの拡張子
file_extention = '.tsv'

# マスタファイル選択ダイアログの表示
root = tkinter.Tk()
root.withdraw()
fTyp = [("","*")]
iDir = os.path.abspath(os.path.dirname(__file__))
tkinter.messagebox.showinfo('類似度算出ツール','比較マスタファイルを選択してください')
master_file = tkinter.filedialog.askopenfilename(filetypes = fTyp, initialdir = iDir)

if master_file == '':
    sys.exit()

# 判定対象ファイル選択ダイアログの表示
root = tkinter.Tk()
root.withdraw()
fTyp = [("","*")]
iDir = os.path.abspath(os.path.dirname(__file__))
tkinter.messagebox.showinfo('類似度算出ツール','比較対象ファイルを選択してください')
target_file = tkinter.filedialog.askopenfilename(filetypes = fTyp, initialdir = iDir)

if target_file == '':
    sys.exit()

master_data = []
target_data = []

# tsvファイル読み込み
with open(master_file, "r", encoding='utf-8-sig') as dpf:
    # 辞書として読み込む
    reader = csv.DictReader(dpf, delimiter='\t')
    for row in reader:
        master_data.append(row)

with open(target_file, "r", encoding='utf-8-sig') as dvf:
    reader = csv.DictReader(dvf, delimiter='\t')
    for row in reader:
        target_data.append(row)

print('処理中です...')

# 対象データごとに類似度を判定
for target in target_data:
    # 類似度の最大値
    max_ratio = 0
    highest_ratio_name = ''
    highest_ratio_id = ''
    for master in master_data:
        ratio = difflib.SequenceMatcher(None, target['比較対象'], master['比較対象']).ratio()
        # 最大値を更新
        if ratio > max_ratio:
            max_ratio = ratio
            highest_ratio_name = master['比較対象']
            highest_ratio_id = master['id']
    target['最も近い語'] = highest_ratio_name
    target['最も近い語のID'] = highest_ratio_id
    target['類似度'] = '{:.2%}'.format(max_ratio)

# 現在日時をファイル名に埋め込むための準備
now_str = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
save_file = save_dir + '/' + save_filename + '_' + now_str + file_extention

# tsvに出力
with open(save_file, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['id', '比較対象', '最も近い語のID', '最も近い語', '類似度'], delimiter='\t')
    writer.writeheader()
    writer.writerows(target_data)

print('ファイルの実行場所に結果を出力しました。')