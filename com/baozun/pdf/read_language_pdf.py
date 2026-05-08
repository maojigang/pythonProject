import PyPDF2
import re


def read_pdf_with_pypdf2_new(pdf_path):
    text = []
    try:
        with open(pdf_path, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            page_num = len(pdf_reader.pages)
            print(f"PDF总页数：{page_num}")
            # 遍历每一页提取文本
            for page in pdf_reader.pages:
                # 提取当前页文本
                page_text = page.extract_text()
                if page_text:
                    result = re.split(r'\n', page_text)
                    temp = []
                    total = len(result)
                    nexIndex = 0
                    for rs in result:
                        nexIndex += 1
                        temp.append(rs)
                        if rs.endswith(".") or rs.endswith("?"):
                            text.append("".join(temp) + '\n')
                            temp.clear()
                    if len(temp):
                        text.append("".join(temp) + '\n')
        return text
    except Exception as e:
        print(f"读取失败：{e}")
        return ""


def read_pdf_new():
    pdf_path = r'D:\u2026\EP53-The City Beneath the City.pdf'
    write_path = r'D:\u2026\city.txt'
    content = read_pdf_with_pypdf2_new(pdf_path)
    with open(write_path, 'w', encoding='utf-8') as f:
        for item in content:
            if item is not None:
                f.write(item + '\n')


if __name__ == "__main__":
    read_pdf_new()


