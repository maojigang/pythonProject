import sys
import json
import pandas as pd

# 1. 读取 JSON 文件
json_file_path = "D:\\file\\Downloads\\test\\shop.txt"  # 替换为你的JSON文件路径
excel_file_path = 'D:\\file\\Downloads\\test\\output.xlsx'  # 替换为输出 Excel 路径

with open(json_file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)
df = pd.DataFrame(data)
df.to_excel(excel_file_path, index=False)
