import pandas as pd
import os


def print_sql():
    newPath = r'C:\Users\xxx\Downloads\新登录名20260512-new.xlsx'
    excel_data = pd.read_excel(newPath)
    excel_data = excel_data.values
    value_list = ['\'' + str(item[1]) + '\'' for item in excel_data]
    print(','.join(value_list))
    # batch_size = 9000
    # for i in range(0, len(excel_data), batch_size):
    #     batch = excel_data[i:i + batch_size]
    #     # 文件名：data_0.txt, data_1.txt...
    #     filename = f"data_{i // batch_size}.txt"
    #     path = r'C:\Users\maojigang\Downloads'
    #     newPath = os.path.join(path, filename)
    #     with open(newPath, "w", encoding="utf-8") as f:
    #         for item in batch:
    #          f.write(f'update ua_user set username = \'{item[1]}\', last_modified_date = \'2026-05-12 23:00:00\' where username = \'{item[0]}\';\n')




if __name__ == '__main__':
    print_sql()