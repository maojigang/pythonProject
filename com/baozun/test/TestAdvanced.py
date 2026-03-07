import asyncio
import time
import queue
import dis
from typing import Tuple


class Person:
    def __init__(self, name):
        self.name = name

    @classmethod
    def createPerson(cls, name):
        print('-------')
        return cls(name)

    @staticmethod
    def query():
        return 'zs'
    
    def __getattr__(self, age):
        print(f'属性不存在')

    def __str__(self):
        return f'age={self.age}'


def testPerson():
    person = Person.createPerson("zs")
    person.query()
    print(person.name)

def testAttr():
    person = Person('zs')
    print(hasattr(person, 'name'))
    setattr(person, 'name1', '1')
    print(hasattr(person, 'name1'))
    value = getattr(person, 'name222', 5)
    print(value)

def testOther():
    class Config:
        def __init__(self):
            self.timeout = 30
            self.retry_count = 3

    config = Config()
    timeout_value = getattr(config, "timeout1", 60)  # 存在则返回值，否则返回60
    print(timeout_value)  # 输出: 30


class Man:
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name + '_1'

    @name.setter
    def name(self, name):
        self._name = name + '_2'

    def __getattribute__(self, item):
        print(f'访问属性={item}')
        return super().__getattribute__(item)

def testProperty():
    m = Man('zs')
    m.name = 'ls'
    print(m.name)
    print(m.__dict__)
    print(Man.__dict__)

async def task(name, delay):
    print(f"任务 {name} 开始（延迟 {delay} 秒）")
    await asyncio.sleep(delay)
    return f"任务 {name} 完成"

async def main():
    # 定义不同延迟的任务
    tasks = [
        asyncio.create_task(task("A", 3)),
        asyncio.create_task(task("B", 1)),
        asyncio.create_task(task("C", 2))
    ]

    # 按完成顺序处理结果
    for done_task in asyncio.as_completed(tasks):
        result = await done_task
        print(f"收到结果：{result}（当前时间：{time.strftime('%H:%M:%S')}）")

def testAsyncIo():
    asyncio.run(main())


def testQueue():
    q = queue.Queue(maxsize=3)
    q.put(1)
    q.put(2)
    q.put(3)
    print(q.qsize())
    for _ in range(0, 4):
        print(q.get_nowait())

def testDis():
    dis.dis(testQueue)


def testLambda():
    f = lambda x: x + 1
    print(list(map(f, [1, 3])))


def testTuple() -> Tuple:
    return 1, 3, 'a'

def testTuple_1():
    a, b, c = testTuple()
    print(a)

def testTupleFor():
    ls = [('a', 1), ('b', 2)]
    for k, v in ls:
        print(f'k={k}, v={v}')
    value = [{k: v} for k, v in ls]
    print(value)
    print(list(ls))

if __name__ == '__main__':
    testPerson()