from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


def parse_dynamic_page(url):
    """
    用Playwright加载动态页面，再用BS4解析
    """
    # 启动Playwright并打开浏览器
    with sync_playwright() as p:
        # 启动无头Chrome（headless=False可显示浏览器窗口，方便调试）
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # 访问目标网址，等待页面完全加载（包括JS）
        # wait_until="load"：等待页面所有资源加载完成
        page.goto(url, wait_until="load")

        # 可选：等待特定元素加载（应对延迟加载的内容）
        # page.wait_for_selector(".dynamic-content", timeout=10000)
        page.screenshot(path=r'D:\file\Downloads\font\a.png')
        # 获取加载完成后的完整HTML源码
        html = page.content()

        # 关闭浏览器
        browser.close()

        # 交给BS4解析
        soup = BeautifulSoup(html, "lxml")

        # 示例：提取动态加载的内容（根据目标网站调整）
        # 假设目标内容在class为dynamic-content的div里
        imgs = soup.select('.mod-kv > img')
        src = imgs[0].get('src')
        dynamic_content = soup.find("div", class_="dynamic-content")
        if dynamic_content:
            print("动态内容：", dynamic_content.text.strip())
        else:
            print("未找到动态内容")


# 测试（替换为你要爬取的动态网页URL）
if __name__ == "__main__":
    target_url = "https://pdp-web.baozun.com/p/6944f09162119a002986cf47?tpl=n8t3whxvy&opCode=ikea&saasTenantCode=baozun"  # 替换为真实动态网页
    parse_dynamic_page(target_url)