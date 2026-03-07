import requests
import json
import time


def jddjBatchPull(filePath: str, pullBatchId: str, operatorId="postMan"):
    with open(filePath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    url = 'http://ddc-adapter-jddj.baozun.com/ddc-adapter-jddj/salesUnit/syncProductByShopCode'
    for d in data:
        dataReq = dict(catalog='APPLE', tenantCode='Apple_Distributor', channel='JDDJ', channelCode='JDDJ', toSnap=True,
                       pullStatus='ALL',
                       pullBatchId=pullBatchId, operatorId=operatorId, operatorUser=operatorId, source='postMan',
                       msgNotice=False)
        dataReq['shopCode'] = d['shopCode']
        dataReq['shopName'] = d['shopName']
        result = requests.post(url, headers={'catalog': 'APPLE', 'tenantCode': 'Apple_Distributor'}, json=dataReq)
        print(f"{d['shopCode']} 请求结果：{result.json()}")


def querySalesUnitSnap(shopCode, heads):
    queryUrl = 'https://ross-api.baozun.com/ddc-pem-service/salesUnitSnapshot/list/snapShot'
    reqJson = {'catalog': 'APPLE', 'saasTenantCode': 'Apple_Distributor', 'channel': 'MTSG',
               'pfStatus': ["6", "2", "4"], "channelCode": 'MTSG', 'operatorId': 'system', 'operatorUser': 'system',
               'shopCode': shopCode, 'pageSize': 20}

    execWhile = True
    page = 0
    ids = []
    while execWhile:
        page += 1
        reqJson['page'] = page
        result = requests.post(queryUrl, headers=heads, json=reqJson)
        resultJson = result.json()
        if resultJson['code'] != '0':
            raise ValueError('请求失败')
        data = resultJson['data']
        if type(data) != dict or data is None or data['content'] is None or len(data['content']) == 0:
            execWhile = False
            continue
        for content in data['content']:
            ids.append(content['id'])
    return ids


def pushSalesUnitSnopt(shopCode):
    heads = {'catalog': 'APPLE', 'saasTenantCode': 'Apple_Distributor',
             'saastenanttoken': '0v6uf0a969f140e312a747fb10d683f47c92831753866478795',
             'token': 'eyJjb2RlIjoiOGRlYjQ3MmU0MjJlNGE3YWJkNzNlNjVjMGNmZmJlN2MiLCJzYWFzVGVuYW50Q29kZSI6IkFwcGxlX0Rpc3RyaWJ1dG9yIiwiaXAiOiIyMjAuMTk2LjU3LjI0NCIsImJyb3dzZXJOYW1lIjoiQ2hyb21lIDEzIn0='}
    ids = querySalesUnitSnap(shopCode, heads)
    if len(ids) == 0:
        return
    pushUrl = 'https://ross-api.baozun.com/ddc-pem-service/salesUnitSnapshot/snapShot/push'
    reqJson = {'operatorId': 'ross-E8DJ4', 'operatorUser': 'ross-E8DJ4', 'ignoreMd5': True}
    reqJson['subscriberIds'] = ['617fc0c42f46ab00012e58b9']
    reqJson['ids'] = ids
    result = requests.post(pushUrl, headers=heads, json=reqJson)
    resultJson = result.json()
    print(f"{shopCode} 请求结果：{resultJson}")
    time.sleep(5)


def execJddjPull():
    taskId = 'pull_' + str(time.time_ns())[:10]
    jddjBatchPull(r'D:\u02\jddj\pull.json', taskId)


if __name__ == '__main__':
    execJddjPull()
