import PyPDF2
import re
import os

def read_pdf_with_pypdf2(pdf_path):
    """
    读取PDF纯文本（PyPDF2）
    :param pdf_path: PDF文件路径
    :return: 提取的文本内容
    """
    text = []
    try:
        # 以二进制模式打开PDF
        with open(pdf_path, 'rb') as f:
            # 创建PDF阅读器对象
            pdf_reader = PyPDF2.PdfReader(f)

            # 获取PDF总页数
            page_num = len(pdf_reader.pages)
            print(f"PDF总页数：{page_num}")

            # 遍历每一页提取文本
            for page in pdf_reader.pages:
                # 提取当前页文本
                page_text = page.extract_text()
                if page_text:
                    result = re.split(r'\d', page_text)
                    result = [test(item) for item in result if item and item is not None]
                    text += result
                    #print(result)

        return text
    except Exception as e:
        print(f"读取失败：{e}")
        return ""

def test(txt):
    #txt = 'levy英:/\'levi/美:/\'levi/n. 征收；征兵，征税 vt. 征收（税等）；征集（兵等）'
    res = txt.split('英:')
    if len(res) == 2:
        r1 = res[1].split('美:')[1]
        result = res[0] + ' ' + add_space_after_second_slash_simple(r1)
        return result.replace('\n', '')
    return None

def add_space_after_second_slash_simple(text):
    """极简版：分割后在第二个 / 后加空格"""
    # 按 / 分割成列表
    parts = text.split('/')
    if len(parts) >= 3:  # 分割后至少3部分（说明有2个 /）
        # 拼接：第一部分 + / + 第二部分 + /  + 空格 + 剩余部分
        processed_text = f"{parts[0]}/{parts[1]}/ {''.join(parts[2:])}"
        return processed_text
    return text

def read_pdf():
    pdf_path = r'D:\u2026\所有生词本_20260222_1903.pdf'
    write_path = r'D:\u2026\所有生词本_202603_new.txt'
    content = read_pdf_with_pypdf2(pdf_path)
    index = 0
    with open(write_path, 'w', encoding='utf-8') as f:
        for item in content:
            if item is not None:
                index += 1
                value = str(index) + '. ' + item
                f.write(value + '\n')

def split_txt():
    txt_path = r'D:\u2026\所有生词本_202603_new.txt'
    with open(txt_path, 'r', encoding='utf-8') as f:
        context = f.readlines()
        index = 0
        while len(context) > 0:
            index += 1
            read_context = context[:300]
            context = context[300:]
            write_path = os.path.join('D:\\u2026', '生词本_'+ str(index) + '.txt')
            with open(write_path, 'w', encoding='utf-8') as ff:
                for item in read_context:
                    ff.write(item)

if __name__ == "__main__":
    split_txt()

