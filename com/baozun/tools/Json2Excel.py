import json
import pandas as pd
import os


def json2Excel(json_file_path: str, excel_file_path: str):
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    df.to_excel(excel_file_path, index=False)
    print('*' * 10 + '完成' + '*' * 10)


if __name__ == '__main__':
    basePath = r'D:\file\Downloads\test'
    inPath = os.path.join(basePath, 'shop.txt')
    outPath = os.path.join(basePath, 'output.xlsx')
    json2Excel(inPath, outPath)
