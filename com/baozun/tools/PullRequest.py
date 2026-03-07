import requests
import json
import time


def writeLog(logPath, logTxt):
    with open(logPath, 'a', encoding='utf-8') as f:
        f.write(logTxt + '\n')


def checkExecRequest(pullTaskId, execNum):
    waitMaxNum = 60
    waitNumber = 0
    execWhile = True
    while execWhile:
        requestUrl = 'http://ddc-adapter-migration.baozun.com/ddc-adapter-migration/meituan/countTaskNum?taskId=' + pullTaskId
        realExecNum = requests.get(requestUrl).json()['data']
        if not (execNum - realExecNum >= waitMaxNum):
            return
        waitNumber += 1
        print(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}等待中,等待次数={waitNumber},请求数量={execNum},执行数量={realExecNum}")
        time.sleep(2)


### request请求
def meituanPull(pullBatchId, shopCode, shopName, operatorId='postMan', totalNum=0, execNum=0):
    meituanPullUrl = "http://ddc-adapter-migration.baozun.com/ddc-adapter-migration/meituan/asyncPull"
    reqJson = {'pullStatus': 'ALL', 'toSnap': True, 'channel': 'MTSG', 'channelCode': 'MTSG'}
    reqJson['shopCode'] = shopCode
    reqJson['shopName'] = shopName
    reqJson['catalog'] = 'APPLE'
    reqJson['tenantCode'] = 'Apple_Distributor'
    reqJson['operatorId'] = operatorId
    reqJson['pullBatchId'] = pullBatchId
    result = requests.post(meituanPullUrl, json=reqJson)
    execTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    printLog = f"{execTime},任务ID={pullBatchId},总数量={totalNum},执行数量={execNum},剩余数量={totalNum - execNum},shopCode={reqJson['shopCode']} 请求结果：{result.json()}"
    print(printLog)
    return printLog


def execMeituanPull(importPath: str, outPath: str, taskId: str, startShopCode: str):
    execNum = 0
    checkExecNum = 0
    start = startShopCode is None or startShopCode == ''
    with open(importPath, 'r', encoding='utf-8') as f:
        dataJson = json.load(f)
        totalNum = len(dataJson)
        print(f"任务ID={taskId},总数={totalNum}")
        for data in dataJson:
            if not start:
                start = data['shopCode'] == startShopCode
                execNum += 1
                continue
            checkExecRequest(taskId, checkExecNum)
            returnLog = meituanPull(taskId, data['shopCode'], data['shopName'], totalNum=totalNum, execNum=execNum + 1)
            execNum += 1
            checkExecNum += 1
            writeLog(outPath, returnLog)
            time.sleep(0.4)


def simpleExecMeituanPull(importPath: str, outPath: str):
    taskId = 'pull_' + str(time.time_ns())[:10]
    startShopCode = None
    execMeituanPull(importPath, outPath, taskId, startShopCode)


if __name__ == '__main__':
    simpleExecMeituanPull(r'D:\u02\meituan\pull.json', r'D:\u02\meituan\log.txt')
