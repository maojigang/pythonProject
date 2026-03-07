import time
import datetime

print(time.localtime())
print(time.time())
print(time.gmtime())
print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))

print(datetime.datetime.today())
print(datetime.datetime.now())
print(datetime.datetime.utcnow())
print('---------------------------------')
print(datetime.datetime.fromtimestamp(time.time()))
print(datetime.datetime.utcfromtimestamp(time.time()))
print(datetime.datetime.combine(datetime.date(2019, 12, 1), datetime.time(10, 10, 10)))
print(datetime.datetime.min)
print(datetime.datetime.max)

print('---------------------------------')

t = time.time()

print(t)  # 原始时间数据
print(int(t))  # 秒级时间戳
print(int(round(t * 1000)))  # 毫秒级时间戳
print(int(round(t * 1000000)))  # 微秒级时间戳

print('---------------------------------')
def getName():
    print('getName')
    return 'zs'


def setName(a):
    print(a * 10)


# 匿名函数
myValue = lambda x, y : x - y


class Cat:
    color = 'red'
    name = ''
    def __init__(self, name):
        print('color --- {}'.format(self.color))

    def doing(self, name, thing):
        self.name = name
        print("{0} === {1} ---- {2}".format(self.name, thing, self.color))


class superCat(Cat):

    def __init__(self):
        self.color = 'blue'
        super().__init__('hh')

    def doing(self, name, thing):
        super().doing(name, thing)

