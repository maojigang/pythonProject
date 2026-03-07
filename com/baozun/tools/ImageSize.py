
import requests
from PIL import Image
from io import BytesIO
import json
import copy

def get_image_file_size(image_url):
    """
    仅获取图片文件大小
    """
    try:
        response = requests.head(image_url)
        response.raise_for_status()
        file_size = int(response.headers.get('content-length', 0))

        # 下载图片以获取尺寸信息
        img_response = requests.get(image_url)
        img_response.raise_for_status()

        # 使用PIL打开图片并获取尺寸
        img = Image.open(BytesIO(img_response.content))
        width, height = img.size

        split = image_url.split('.')
        suffix = split[len(split) - 1] if len(split) > 1 else ''

        return {
            'file_size_bytes': file_size,
            'file_size_kb': round(file_size / 1024, 2),
            'file_size_mb': round(file_size / (1024 * 1024), 2),
            'width': width,
            'height': height,
            'suffix': suffix
        }
    except Exception as e:
        return {
            'file_size_bytes': 0,
            'file_size_kb': 0,
            'file_size_mb': 0,
            'error': str(e)
        }


'''
主图：图片尺寸为1200 * 1200，单张不超过1024K，仅支持jpg，jpeg式，最多可上传12张图片
列表图：图片尺寸为950 * 1200，单张不超过1024K，仅支持jpg，jpeg格式
透明图：图片尺寸为无限制，单张大小100K和600K之间，仅支持png格式，最多可上传1张图片。
实物吊牌&标签图：图片尺寸为750 * 1600（max），单张大小不超过1024K，仅支持jpg，jpeg格式，最多可上传5张图片
PC&Mobile：请上传宽度不小于640px，高度不超过宽度3倍，不超过1024K的图片，仅支持jpg，jpeg格式，最多可上传50张图片
'''


def checkResource(resourceList):
    copyNewResourceList = copy.deepcopy(resourceList)
    for resource in copyNewResourceList:
        if resource['type'] == '主图':
            res = resource['assets']
            result = [rs for rs in res if rs['size'] > 1024 or rs['suffix'] != 'jpg' or rs['width'] != 1200 or rs['height'] != 1200]
            resource['assets'] = result
        elif resource['type'] == '列表图':
            res = resource['assets']
            result = [rs for rs in res if rs['size'] > 1024 or rs['suffix'] != 'jpg' or rs['width'] != 950 or rs['height'] != 1200]
            resource['assets'] = result
        elif resource['type'] == '透明图':
            res = resource['assets']
            result = [rs for rs in res if rs['size'] > 600 or rs['size'] < 100 or rs['suffix'] != 'png' ]
            resource['assets'] = result
        elif resource['type'] == '实物吊牌&标签图':
            res = resource['assets']
            result = [rs for rs in res if rs['size'] > 1024 or rs['suffix'] != 'jpg' or rs['width'] != 750 or rs['height'] > 1600]
            resource['assets'] = result
        elif resource['type'] == 'PC' or resource['type'] == 'Mobile':
            res = resource['assets']
            result = [rs for rs in res if rs['size'] > 1024 or rs['suffix'] != 'jpg' or rs['width'] != 750 or rs['height'] > rs['width'] * 3]
            resource['assets'] = result
    return copyNewResourceList


def getResourceImageSize():
    txtPath = r'D:\u02\vipCheck\vip.txt'
    with open(txtPath, 'r', encoding='utf-8') as file:
        resource = json.load(file)
    rs = resource if isinstance(resource, list) else resource['resources']
    resourceList = []
    for r in rs:
        type = r['type']
        resourceResult = []
        for asset in r['assets']:
            if type == 'PC' or type == 'Mobile':
                if not ('replaceUrl' in asset.keys() and asset['replaceUrl'] is not None and len(asset['replaceUrl']) > 0):
                    continue
                for image in asset['replaceUrl']:
                    res = get_image_file_size(image)
                    size = res['file_size_kb']
                    resourceResult.append(
                        {'size': size, 'width': res['width'], 'height': res['height'], 'suffix': res['suffix'], 'url': image})
            else:
                res = get_image_file_size(asset['url'])
                size = res['file_size_kb']
                resourceResult.append(
                    {'size': size, 'width': res['width'], 'height': res['height'], 'suffix': res['suffix'], 'url': asset['url']})
        resourceList.append({'type': type, 'assets': resourceResult})

    checkResult = checkResource(resourceList)
    # newResourceList = json.dumps(resourceList, ensure_ascii=False)
    # print(newResourceList)
    print(json.dumps(checkResult, ensure_ascii=False, indent=2))



if __name__ == '__main__':
    getResourceImageSize()
