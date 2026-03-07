import requests
import json
import os
import time

basePath = 'D:\\file\\historyDownloads\\program\\'


### request请求

def jddjPull():
    data = dict(catalog='APPLE', tenantCode='Apple_Distributor', channel='JDDJ', channelCode='JDDJ', toSnap=True,
                pullStatus='ALL',
                shopCode='20232088', shopName='京东-陕西众合太原龙城万达店', pullBatchId='20250730-ALL-01',
                operatorId='730', operatorUser='730', source='730', msgNotice=False)
    url = 'http://ddc-adapter-jddj.baozun.com/ddc-adapter-jddj/salesUnit/syncProductByShopCode'
    result = requests.post(url, headers={'catalog': 'APPLE', 'tenantCode': 'Apple_Distributor'}, json=data)
    print(result.json())


def jddjBatchPull(fileName, operatorId="postMan"):
    json_file_path = os.path.join(basePath, fileName)
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    pullBatchId = '20250730-ALL'
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


def meituanPull(pullBatchId, shopCode, shopName, operatorId='postMan'):
    meituanPullUrl = "http://ddc-adapter-migration.baozun.com/ddc-adapter-migration/meituan/asyncPull"
    reqJson = {'pullStatus': 'ALL', 'toSnap': True, 'channel': 'MTSG', 'channelCode': 'MTSG'}
    reqJson['shopCode'] = shopCode
    reqJson['shopName'] = shopName
    reqJson['catalog'] = 'APPLE'
    reqJson['tenantCode'] = 'Apple_Distributor'
    reqJson['operatorId'] = operatorId
    reqJson['pullBatchId'] = pullBatchId
    result = requests.post(meituanPullUrl, json=reqJson)
    print(f"{reqJson['shopCode']} 请求结果：{result.json()}")


def querySalesUnitSnap(shopCode, heads):
    queryUrl = 'https://ross-api.baozun.com/ddc-pem-service/salesUnitSnapshot/list/snapShot'
    reqJson = {'catalog' : 'APPLE', 'saasTenantCode': 'Apple_Distributor', 'channel': 'MTSG',
               'pfStatus': ["6","2","4"],
               "channelCode": 'MTSG', 'operatorId': 'system', 'operatorUser': 'system' }
    reqJson['shopCode'] = shopCode
    reqJson['pageSize'] = 20

    execWhile = True
    page = 0
    ids = []
    while execWhile:
        page += 1
        reqJson['page'] = page
        result = requests.post(queryUrl, headers=heads, json=reqJson)
        resultJson = result.json()
        if(resultJson['code'] != '0'):
            raise ValueError('请求失败')
        data = resultJson['data']
        if(type(data) != dict or data is None  or data['content'] is None or len(data['content']) == 0):
            execWhile = False
            continue
        for content in data['content']:
            ids.append(content['id'])
    return ids

def pushSalesUnitSnopt(shopCode):
    heads = {'catalog': 'APPLE', 'saasTenantCode': 'Apple_Distributor'}
    heads['saastenanttoken'] = '0v6uf0a969f140e312a747fb10d683f47c92831753866478795'
    heads['token'] = 'eyJjb2RlIjoiOGRlYjQ3MmU0MjJlNGE3YWJkNzNlNjVjMGNmZmJlN2MiLCJzYWFzVGVuYW50Q29kZSI6IkFwcGxlX0Rpc3RyaWJ1dG9yIiwiaXAiOiIyMjAuMTk2LjU3LjI0NCIsImJyb3dzZXJOYW1lIjoiQ2hyb21lIDEzIn0='
    ids = querySalesUnitSnap(shopCode, heads)
    if(len(ids) == 0):
        return
    pushUrl = 'https://ross-api.baozun.com/ddc-pem-service/salesUnitSnapshot/snapShot/push'
    reqJson = {'operatorId': 'ross-E8DJ4', 'operatorUser': 'ross-E8DJ4', 'ignoreMd5': True}
    reqJson['subscriberIds'] = ['617fc0c42f46ab00012e58b9']
    reqJson['ids'] = ids
    result = requests.post(pushUrl,headers=heads, json=reqJson)
    resultJson = result.json()
    print(f"{shopCode} 请求结果：{resultJson}")
    time.sleep(5)

#pushSalesUnitSnopt('103000')
## jddjBatchPull('apple_pull.txt');



