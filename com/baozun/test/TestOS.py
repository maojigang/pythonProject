import os

def test_os():
    print(os.path.abspath('.'))
    print(os.getcwd())

    items = os.listdir('.')
    print(items)

    # 检查操作系统类型
    if os.name == 'nt':  # Windows系统
        print('Windows系统')
    elif os.name == 'posix':  # Unix/Linux/MacOS系统
        print('Unix/Linux/MacOS系统')

    for root, dirs, files in os.walk("."):
        for file in files:
            print(os.path.join(root, file))

if __name__ == '__main__':
    test_os()

