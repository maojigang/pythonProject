import requests
import json

# url = 'http://ddc-pem-sit.cloud.bz/ddc-pem-service/salesUnit/list'
# data = {"pageSize":10,"page":1,"channel":"CK天猫测试渠道","operatorId":"ross-NE7m2"};
# result = requests.post(url, headers ={'catalog': 'JD02', 'tenantCode': 'baozun'}, json = data )
# r_data = result.json()['data']['content']
# print(r_data)


# json_file_path = 'D:\\file\\Downloads\\apple_pull.txt';
# with open(json_file_path, 'r', encoding='utf-8') as f:
#     data = json.load(f)
# pullBatchId = '20250730-ALL'
# url = 'http://ddc-adapter-jddj.baozun.com/ddc-adapter-jddj/salesUnit/syncProductByShopCode'
# for d in data:
#     dataReq = dict(catalog='APPLE', tenantCode='Apple_Distributor', channel='JDDJ', channelCode='JDDJ',
#                 shopCode= d['shopCode'], shopName=d['shopName'],  pullBatchId = pullBatchId ,
#                 toSnap = True, pullStatus='ALL', operatorId='730',
#                 operatorUser='730', source='730',  msgNotice=False)
#     result = requests.post(url, headers={'catalog': 'APPLE', 'tenantCode': 'Apple_Distributor'}, json=dataReq)
#     print(f"{ d['shopCode']} 请求结果：{result.json()}")

data = dict(catalog='APPLE', tenantCode='Apple_Distributor', channel='JDDJ', channelCode='JDDJ',
            shopCode='20232088', shopName='京东-陕西众合太原龙城万达店',  pullBatchId='20250730-ALL-01',
            toSnap = True, pullStatus='ALL', operatorId='730',
            operatorUser='730', source='730',  msgNotice=False)

url = 'http://ddc-adapter-jddj.baozun.com/ddc-adapter-jddj/salesUnit/syncProductByShopCode'
result = requests.post(url, headers ={'catalog': 'APPLE', 'tenantCode': 'Apple_Distributor'}, json = data )
print(result.json())
