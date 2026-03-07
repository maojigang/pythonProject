import string
import time
from concurrent.futures import ThreadPoolExecutor


def task(n):
    time.sleep(1)
    return f"任务{n}返回"


def testFuture():
    with ThreadPoolExecutor(max_workers=3) as executor:
        future1 = executor.submit(task, 1)
        future2 = executor.submit(task, 2)
        print(future1.result(), future2.result())


def testFutureMap():
    with ThreadPoolExecutor(max_workers=3) as exec:
        result = exec.map(task, [1, 2, 3, 4, 5])
        for ts in result:
            print(ts)


def taskNew(n, m, k):
    time.sleep(1)
    return f"任务NEW, n={n}, m={m}, k={k}"


def testNewTask():
    with ThreadPoolExecutor(max_workers=2) as executor:
        result = executor.submit(taskNew, m=1, k=2, n=3)
        print(result.result())


if __name__ == '__main__':
    testNewTask()
