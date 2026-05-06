import re

# 1 如果直接给出字符，则表示精确匹配
# 2 \d 表示数字， \w 表示字母或数字， . 可以匹配任意字符，\s 表示空白符，包括Tab
# 3 * 表示任意长度，+ 表示至少一个字符，？ 表示0或1个字符，{n} 表示n个字符，{n,m} 表示n到m个字符
# 如 \d{3}\s+\d{3,8}
# - 是特殊字符，需要\转义 \-

# 更精确的匹配范围 表示 []
# 如 [0-9a-zA-Z\_] 可以匹配一个数字，字母，或者下划线
# A|B 可以匹配A，B
# ^ 表示行的开头， ^\d 表示必须以数字开头
# $ 表示行的结束，\d$ 表示必须以数字结束
def test_regex():
    txt = 'hello  world'
    result = re.split(r'\s{1}', txt)
    print(result)
    print('\n'.join([' '.join(['%s*%s=%-2s' % (y, x, x * y) for y in range(1, x + 1)]) for x in range(1, 10)]))

def test_su():
    result = re.sub('星期一', '星期二', '今天星期一, 星期一是个工作的第一天', count=1)
    print(result)
    ab = 5 / 3
    newValue = f"{ab:.2f}"
    print(newValue)
    print("{:.2f}".format(ab))
    print(f"{ab:.2f}")

    tup = (1, 3)
    a, b = tup
    print(f"{a}={b}")

    l1 = [2, 3, 4, 5]
    c, d = l1[:2]
    print(f"{c}={d}")

    s1 = '''aaabcddfdsdd'''
    print(s1 + "中国")

if __name__ == '__main__':
    test_regex()
