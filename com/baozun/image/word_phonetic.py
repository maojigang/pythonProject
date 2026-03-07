import requests
import json
from typing import Dict, Optional


class WordPhoneticTool:
    def __init__(self):
        # 配置API（这里使用免费的有道词典API示例，实际使用需自行申请）
        self.api_url = "https://dict.youdao.com/jsonapi"

    def get_phonetic(self, word: str) -> Optional[Dict]:
        """获取单词的音标和基本释义"""
        if not word or not word.isalpha():
            return None

        try:
            # 构造请求参数
            params = {
                "q": word,
                "doctype": "json"
            }

            # 发送请求
            response = requests.get(self.api_url, params=params, timeout=10)
            data = json.loads(response.text)

            # 解析音标（美式和英式）
            phonetic_data = {}

            # 提取音标信息（不同API返回格式可能不同）
            if "basic" in data:
                # 美式音标
                if "usphone" in data["basic"]:
                    phonetic_data["us"] = data["basic"]["usphone"]
                # 英式音标
                if "ukphone" in data["basic"]:
                    phonetic_data["uk"] = data["basic"]["ukphone"]
                # 基本释义
                if "explains" in data["basic"]:
                    phonetic_data["meaning"] = data["basic"]["explains"][0] if data["basic"]["explains"] else ""

            return phonetic_data if phonetic_data else None

        except Exception as e:
            print(f"获取音标失败（{word}）: {str(e)}")
            return None

    def add_phonetic_to_words(self, words: list) -> list:
        """为单词列表添加音标"""
        result = []
        for word in words:
            word = word.strip().lower()
            phonetic = self.get_phonetic(word)
            if phonetic:
                item = {
                    "word": word,
                    "phonetic": phonetic
                }
                result.append(item)
            else:
                result.append({"word": word, "phonetic": "未找到音标"})
        return result


if __name__ == "__main__":
    # 示例用法
    tool = WordPhoneticTool()

    # 要添加音标的单词列表
    words = ["apple", "banana", "computer", "beautiful", "congratulations"]

    # 获取带音标的结果
    result = tool.add_phonetic_to_words(words)

    # 打印结果
    for item in result:
        print(f"{item['word']}:")
        if isinstance(item['phonetic'], dict):
            print(f"  美式音标: {item['phonetic'].get('us', '无')}")
            print(f"  英式音标: {item['phonetic'].get('uk', '无')}")
            print(f"  释义: {item['phonetic'].get('meaning', '无')}")
        else:
            print(f"  {item['phonetic']}")
        print("-" * 50)
