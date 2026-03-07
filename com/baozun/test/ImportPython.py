import TestPython2 as tp2
from TestPython2 import getName
from TestPython2 import myValue

tp2.setName('world ')
print(getName())
print(myValue(10, 6))

cat = tp2.Cat('1')
cat.doing('lili', 'doing')

supCat = tp2.superCat()
supCat.doing("cc", 'aa')

# 指定文件路径
file_path = 'D:\\file\\Downloads\\EZE834_log.txt'

# with open(file_path, 'r', encoding='utf-8') as file:
#     content = file.read()
#     # print(content)
#
#
# with open(file_path, 'r', encoding='utf-8') as file:
#     texts = file.readlines()
#     for line in texts:
#         print(line)


import os

exists = os.path.exists(file_path)
print(exists)
testPath = 'D:\\file\\Downloads\\test\\'
pathList = os.walk('D:\\file\\Downloads\\test\\')
for path, dirs, files in pathList:
    for file in files:
        print(os.path.join(path, file))
    # print(path)
    # print(dirs)
    #print(files)
# os.remove('D:\\file\\Downloads\\test\\test.txt')
splitPath = os.path.splitext(testPath + '1.txt')
print(f"splitPath {splitPath}")

size = os.path.getsize("D:\\file\\Downloads\\test\\1.txt") # 字节
print(size)

import json
# with open(, file_path'r', encoding = 'utf-8') as f:
#     data = json.load(f)
#     for d in data:
#         print(d)
# print(data)


import pandas as pd
# data = pd.read_excel('D:\\file\\Downloads\\周大福数据删除记录.xlsx', usecols=['h1', 'h2'])
# print(data.head(0))
# print(data.values)
#
# data = {'name':['python','java','C++'],'age':[2021,2022,2023],'rank':['1','2','3']}
# df = pd.DataFrame(data)
# df.to_excel(os.path.join(testPath,'file.xlsx'))

# 从字符串读取JSON数据
data_str = '[{"name": "John", "age": 30, "city": "New York"}, {"name": "Doe", "age": 25, "city": "Paris"}]'
data = json.loads(data_str)

# 将JSON转换为DataFrame（对于列表）
df = pd.json_normalize(data)  # 对于单个字典，则不需要此步骤，直接使用pd.DataFrame(data)即可。
# df.to_excel(os.path.join(testPath, 'file1.xlsx'), index=False)


data = {'name':['python','java','C++'],'age':[2021,2022,2023],'rank':['1','2','3']}
df = pd.DataFrame(data)
print(df.columns.tolist())



