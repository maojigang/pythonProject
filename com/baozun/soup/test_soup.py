import requests
from bs4 import BeautifulSoup
import sys

'''
1. find ()：查找单个节点
  返回第一个匹配的节点，无匹配则返回None：
    按class查找（class是Python关键字，需用class_）
    highlight_p = soup.find("p", class_="highlight")
    print(highlight_p.text)
    
    按id查找
    main_div = soup.find(id="main")
    print(main_div.name)
    
    多条件组合查找
    target_p = soup.find("p", attrs={"class": "text", "name": "test"}) 

    按文本内容查找（模糊匹配）
    li = soup.find("li", string=lambda text: "列表项1" in text)
    
2. find_all ()：查找所有匹配节点
   返回列表（无匹配则为空列表
   
    1. 查找所有p标签
    all_p = soup.find_all("p")
    for p in all_p:
        print(p.text)  # 依次输出两个p标签的文本
    
    2. 查找多个标签（传入列表）
    tags = soup.find_all(["h1", "li"])
    print([tag.text for tag in tags])  # ['BS4常用用法', '列表项1', '列表项2']
    
    3. 限制查找数量（limit参数）
    two_li = soup.find_all("li", limit=2)  # 只取前2个
    
    4. 按class多值查找（匹配任意一个class）
    text_p = soup.find_all("p", class_="text")  # 匹配class包含text的p标签
    
3. select ()：CSS 选择器（推荐，灵活）
支持 CSS 选择器语法，返回列表，前端开发者更容易上手
    1. 按标签名
    print(soup.select("title")[0].text)  # 测试页面
    
    2. 按class（.class名）
    print(soup.select(".highlight")[0].text)  # 第二个段落 链接2
    
    3. 按id（#id名）
    print(soup.select("#main h1")[0].text)  # BS4常用用法（嵌套选择）
    
    4. 子选择器（>）
    print(soup.select("div > p")[0].text)  # 第一个段落 链接1
    
    5. 属性选择器
    link = soup.select('a[href="https://example.com"]')[0]
    print(link.text)  # 链接1
    
    6. 多条件
    print(soup.select("p.text.highlight")[0].text)  # 匹配同时有text和highlight类的p标签
'''

def get_webpage_info(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.title.string if soup.title else "无标题"
        book_list = soup.find('ul', attrs={'class': 'chart-dashed-list'})
        return [item.select('h2 > .fleft')[0].text for item in book_list.find_all('li')]
    except requests.exceptions.RequestException as e:
        print(f"请求出错：{e}")
        return None
    except Exception as e:
        print(f"解析出错：{e}")
        return None


def main():
    rs = []
    for i in range(1, 9):
        url = 'https://book.douban.com/latest?subcat=全部&p=%s&updated_at=' % i
        result = get_webpage_info(url)
        if result is not None:
            rs = rs + result
    print(rs)


if __name__ == "__main__":
    main()