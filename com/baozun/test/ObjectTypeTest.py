
def testbase():
    print(type(None))
    print(type(True))
    print(type(1))
    print(type('11'))
    print(type([1, 2, 3]))
    print(type(Person))

    print('***' * 10)

    person = Person()
    print(isinstance(person, Person))
    print(dir( person))

class Person:
    name = ''


if __name__ == '__main__':
    testbase()