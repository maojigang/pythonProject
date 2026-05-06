import pandas as pd
import os
import openpyxl

def test():
    path = r'C:\Users\maojigang\Downloads'
    fileName = '新建 Microsoft Excel 工作表.xlsx'
    newPath = os.path.join(path, fileName)
    excel_data = pd.read_excel(newPath)
    cols = [str(item).replace('\n', '') for item in excel_data.columns]
    cols[0] = '日期'
    dates = [d[0] for d in excel_data.values]
    index = 0
    for col in cols:
        if index != 0:
            data = [d[index] for d in excel_data.values]
            index1 = 0
            vs = []
            for date in dates:
                a = str(data[index1]).replace('↓','').replace('↑','')
                value = f'{date}号的值为：{a}'
                vs.append(value)
                index1 += 1
            p_v = col.strip() + '：' + '，'.join(vs)
            print(p_v)

        index += 1

    pass


if __name__ == "__main__":
    test()