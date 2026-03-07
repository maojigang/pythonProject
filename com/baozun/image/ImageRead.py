import pytesseract
from PIL import Image
import os

def extract_text_from_image(image_path):
    """
    从图片中提取文字
    :param image_path: 图片路径
    :return: 提取的文字字符串
    """
    try:
        # 检查文件是否存在
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"图片文件不存在: {image_path}")

        # 手动指定 tesseract 路径（如果环境变量未配置）
        pytesseract.pytesseract.tesseract_cmd = r'D:\install\Tesseract-OCR\tesseract.exe'

        # 打开图片
        with Image.open(image_path) as img:
            # 可选：预处理图片以提高识别率
            # 转换为灰度图
            img = img.convert('L')
            # 二值化处理（根据图片情况调整阈值）
            threshold = 150
            img = img.point(lambda p: p > threshold and 255)

            # 使用pytesseract提取文字
            # 提取文字，lang参数指定语言，中文为'chi_sim'
            text = pytesseract.image_to_string(img, lang='chi_sim+eng')

            return text.strip()

    except Exception as e:
        print(f"提取文字时出错: {str(e)}")
        return None

if __name__ == '__main__':
    image_path = r'D:\u02\image\testRead2.png'
    text = extract_text_from_image(image_path)
    if text:
        print(text)
    else:
        print("未找到文字")
