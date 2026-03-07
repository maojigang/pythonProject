import random
import string
import json
import time

'''
注释
'''


# 注释

# 字符串
def test_str():
    a = "hello world"
    print(a[:3])
    print(a[3:])  # ello world
    print(a[3:-1])  # lo worl
    print(chr(65))  # A
    print(ord('A'))  # 65
    print(a.upper())  # HELLO WORLD
    print(a.lower())  # hello world
    print(a.capitalize())  # Hello world
    print(a.title())  # Hello World
    print("strip " + " ab ".strip())  # 去白

    print("a %s" % "b c")
    print("{0} {1} haha".format("hello", "world"))
    print(f"图片已保存至：{a}")
    print('a' * 10)
    print('a' + 'b')

    existA = "python"
    print(('th' in existA) == True)

    str = 'fda'
    print(sorted(str))
    print(max(str))
    print(len(str))


# list
def test_list():
    list1 = [1, 'a', 0.5]
    list1.append('b')
    print(list1[1])
    print(list1[1:])
    del list1[1]
    print(list1)
    print(list1.count('a'))
    print(list1.index('b'))

    list2 = [1, 2, 3, 1]
    list2.remove(1)  # 移除首个匹配项
    print(list2)
    print(list2.index(3))
    list2.sort()
    print(list2)

    list3 = list2.copy()
    list3[0] = 12
    print(list2)
    print(list3)


# tuple
def test_tuple():
    tuple1 = (1, 7, 0.5)
    print(tuple1[0])
    print(max(tuple1))
    print(len(tuple1))


# dict
def test_dict():
    dict1 = dict()
    print(dict1)
    print(dict1 is None or len(dict1) == 0)
    print(dict1 is not None and len(dict1) == 0)

    dict2 = {'name': 'zs', 'age': 15}
    print(dict2['name'])

    dict3 = dict(name='22', age=23)
    for key in dict3.keys():
        print(f"key={key}")
    keys = list(dict3.keys())
    print(keys)
    for name, age in dict3.items():
        print(f"{name} {age}")

    # enumerate 迭代
    for index, value in enumerate(dict3):
        print(f"index={index}, value={value}")


def testRandom():
    str = "hello world"
    listStr = list(str)
    print(listStr)
    random.shuffle(listStr)
    print("".join(listStr))
    print("".join(random.choices(string.ascii_letters + string.digits, k=10)))


def testNext():
    data_str = '[{"name": "John", "age": 31, "city": "New York"}, {"name": "John1", "age": 25, "city": "Paris","a":"b"}]'
    data_json = json.loads(data_str)
    v1 = (obj for obj in data_json if obj['name'] == 'John')
    v2 = [obj for obj in data_json if obj['name'] == 'John']
    v3 = next(v1)

    dic = {'name': 'zs', 'age': 1}
    print(dic.items())
    print(dic.keys())
    print("-".join(dic.keys()))
    for idx, (key, value) in enumerate(dic.items()):
        print(f"索引 {idx}：{key} = {value}")

    print("0")


def testTime():
    strTime = time.strftime('%Y-%m-%d %H:%M:%S')
    print(strTime)
    str = '2025-12-05 10:12:44'
    timeValue = time.strptime(str, '%Y-%m-%d %H:%M:%S')
    print(time.mktime(timeValue))
    print(type(time.time()))


def add(a: int, b: int):
    return a + b


def endWithValue(a: int):
    return str(a).endswith('3')


def innerFunction():
    value1 = all([0, 1])
    print(value1)
    seasons = ['Spring', 'Summer', 'Fall', 'Winter']
    print(list(enumerate(seasons)))

    print(eval('1 + 1'))
    print(eval('add(4, 1)'))
    parameter = {"a": 8, "b": 1}
    print(eval('a + b', parameter))
    print('*' * 20)
    filter_value = filter(endWithValue, [1, 3, 5])
    print(list(filter_value))

    nums = [1, 2, 3, 4]
    result = map(lambda x: x * 2, filter(lambda x: x % 2 == 0, nums))
    print(list(result))


def testSlice():
    v1 = list(range(10))
    rs = v1[slice(0, 5, 2)]
    print(rs)


from functools import cmp_to_key

def compare(a, b):
    return len(str(a)) - len(str(b))

def testSort():
    list = [23, 3, 1, 9, 4]
    print(sorted(list))
    print(list.sort())
    print(list)

    strs = ["apple", 2, "cherry", "date"]
    # sorted_strs = sorted(strs, key=len, reverse=True)
    # print(sorted_strs)

    sorted_reslult = sorted(strs, key=cmp_to_key(compare))
    print(sorted_reslult)




if __name__ == '__main__':
    testSort()
