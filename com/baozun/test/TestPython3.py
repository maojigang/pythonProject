import json
def getForValue():
    l1 = [1, 2, 3]
    for i in l1:
        yield i

def nextTest():
    data_str = '[{"name": "John", "age": 31, "city": "New York"}, {"name": "John", "age": 25, "city": "Paris","a":"b"}]'
    jsonData = json.loads(data_str)
    iterJson = iter(jsonData)
    # print(next(iterJson))
    # print(next(iterJson))

    bob = next((item for item in jsonData if item['name'] == 'John'), None)
    print(bob)

    people_over_30 = [item for item in jsonData if item['age'] > 30]
    print(people_over_30)

    ab_sfb = [item for item in jsonData if "a" in item.keys()]
    print(ab_sfb)


if __name__ == '__main__':
    values = getForValue()
    for i in values:
        print(i)

    nextTest()
