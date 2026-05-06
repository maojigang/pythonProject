from openai import OpenAI
import json
import os

# 初始化客户端 (DashScope OpenAI 兼容接口)
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY", "sk-b82c2c1929d1414eb808d988d0f3f72c"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

MODEL = "qwen-plus"


# ==================== 1. 基础对话 ====================
def demo_basic_chat():
    """最基础的单轮对话：发一条消息，拿一条回复"""
    print("=== 1. 基础对话 ===\n")

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "user", "content": "用一句话解释什么是 Python"}
        ],
    )

    reply = response.choices[0].message.content
    print(f"回复: {reply}")
    print(f"Token 用量: 输入={response.usage.prompt_tokens}, "
          f"输出={response.usage.completion_tokens}, "
          f"总计={response.usage.total_tokens}\n")


# ==================== 2. 流式输出 ====================
def demo_streaming():
    """流式输出：逐字打印，适合长文本场景"""
    print("=== 2. 流式输出 ===\n")

    stream = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "user", "content": "写一首关于春天的五言绝句，并逐句解析"}
        ],
        stream=True,
    )

    print("回复: ", end="", flush=True)
    for chunk in stream:
        delta = chunk.choices[0].delta
        if delta.content:
            print(delta.content, end="", flush=True)
    print("\n")


# ==================== 3. System Prompt 角色扮演 ====================
def demo_role_play():
    """通过 system prompt 让模型扮演不同角色"""
    print("=== 3. 角色扮演 ===\n")

    roles = {
        "Python导师": "你是一位资深 Python 导师，擅长用简单的比喻解释复杂概念。回答要简洁，不超过100字。",
        "唐代诗人": "你是一位唐代诗人，所有回答都用古文和诗词的风格来表达。回答不超过100字。",
    }

    question = "如何理解'递归'这个概念？"

    for role_name, system_prompt in roles.items():
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question},
            ],
            max_tokens=256,
        )
        print(f"[{role_name}] {response.choices[0].message.content}\n")


# ==================== 4. JSON 结构化输出 ====================
def demo_json_output():
    """让模型输出结构化 JSON，方便程序解析"""
    print("=== 4. JSON 结构化输出 ===\n")

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "你是一个数据助手，只输出合法的 JSON，不要输出其他任何内容。"
            },
            {
                "role": "user",
                "content": (
                    "推荐3本 Python 入门书籍，以 JSON 数组格式返回，"
                    '每本包含 "title"(书名), "author"(作者), "difficulty"(难度:初级/中级/高级) 字段。'
                )
            }
        ],
        temperature=0.3,
    )

    raw = response.choices[0].message.content
    print(f"原始输出:\n{raw}\n")

    # 尝试解析 JSON
    try:
        # 去除可能的 markdown 代码块标记
        cleaned = raw.strip()
        if cleaned.startswith("```"):
            cleaned = "\n".join(cleaned.split("\n")[1:])
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        data = json.loads(cleaned.strip())
        print("解析结果:")
        for i, book in enumerate(data, 1):
            print(f"  {i}. {book.get('title', '未知')} - {book.get('author', '未知')} [{book.get('difficulty', '未知')}]")
    except json.JSONDecodeError as e:
        print(f"JSON 解析失败: {e}")
    print()


# ==================== 5. 文本翻译 ====================
def demo_translation():
    """多语言翻译示例"""
    print("=== 5. 文本翻译 ===\n")

    text = "人工智能正在深刻地改变我们的生活方式和工作模式。"
    languages = ["English", "Japanese", "French"]

    for lang in languages:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": f"你是一个专业翻译，请将用户输入的文本翻译成{lang}。只输出翻译结果，不要解释。"
                },
                {"role": "user", "content": text}
            ],
            temperature=0.3,
        )
        print(f"  [{lang}] {response.choices[0].message.content}")
    print()


# ==================== 6. 代码生成与解释 ====================
def demo_code_generation():
    """让模型生成代码并解释"""
    print("=== 6. 代码生成 ===\n")

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "你是一个 Python 编程助手。先给出代码，再用中文简要解释关键逻辑。"
            },
            {
                "role": "user",
                "content": "用 Python 实现一个冒泡排序函数，并写一个简单的测试用例。"
            }
        ],
        temperature=0.3,
    )

    print(response.choices[0].message.content)
    print()


# ==================== 7. 多轮对话（带记忆） ====================
def demo_multi_turn():
    """多轮对话：维护 messages 列表实现上下文记忆"""
    print("=== 7. 多轮对话（输入 quit 退出）===\n")

    messages = [
        {"role": "system", "content": "你是一个友好的助手，回答简洁明了。"}
    ]

    while True:
        user_input = input("你: ").strip()
        if not user_input:
            continue
        if user_input.lower() == "quit":
            print("再见！")
            break

        messages.append({"role": "user", "content": user_input})

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            max_tokens=1024,
        )

        reply = response.choices[0].message.content
        messages.append({"role": "assistant", "content": reply})

        print(f"助手: {reply}\n")


# ==================== 8. Temperature 对比 ====================
def demo_temperature():
    """对比不同 temperature 对输出的影响"""
    print("=== 8. Temperature 参数对比 ===\n")

    prompt = "给我的咖啡店取一个有创意的名字"
    temps = [0.0, 0.7, 1.5]

    for temp in temps:
        print(f"[temperature={temp}]")
        for i in range(3):
            response = client.chat.completions.create(
                model=MODEL,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=64,
                temperature=temp,
            )
            name = response.choices[0].message.content.strip().split("\n")[0]
            print(f"  第{i + 1}次: {name}")
        print()


# ==================== 主菜单 ====================
DEMOS = {
    "1": ("基础对话", demo_basic_chat),
    "2": ("流式输出", demo_streaming),
    "3": ("角色扮演", demo_role_play),
    "4": ("JSON 结构化输出", demo_json_output),
    "5": ("文本翻译", demo_translation),
    "6": ("代码生成", demo_code_generation),
    "7": ("多轮对话", demo_multi_turn),
    "8": ("Temperature 对比", demo_temperature),
    "0": ("运行全部（除多轮对话）", None),
}


def main():
    print("=" * 40)
    print("  Qwen (通义千问) API 学习示例")
    print("=" * 40)

    for key, (name, _) in DEMOS.items():
        print(f"  {key}. {name}")
    print(f"  q. 退出")
    print("=" * 40)

    choice = input("请选择 (0-8, q): ").strip()

    if choice == "q":
        return

    if choice == "0":
        for key, (_, func) in DEMOS.items():
            if key not in ("0", "7"):  # 跳过"全部"和交互式多轮对话
                func()
        return

    if choice in DEMOS:
        _, func = DEMOS[choice]
        if func:
            func()
    else:
        print("无效选项")


if __name__ == "__main__":
    main()
