"""
Agent Skills (Function Calling) 学习示例
=========================================
演示如何让 Qwen 模型自主决定调用哪个"技能"（函数），实现智能代理。

依赖: pip install openai
"""
from openai import OpenAI
import json
import os

# 初始化客户端
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY", "sk-b82c2c1929d1414eb808d988d0f3f72c"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

MODEL = "qwen-plus"


# ============================================================
# 第一步：定义 Skills（Python 函数）
# ============================================================

def get_weather(city: str) -> str:
    """模拟获取天气信息"""
    weather_db = {
        "北京": {"temp": 22, "condition": "晴", "humidity": 35},
        "上海": {"temp": 26, "condition": "多云", "humidity": 65},
        "深圳": {"temp": 30, "condition": "小雨", "humidity": 80},
        "成都": {"temp": 20, "condition": "阴", "humidity": 70},
    }
    info = weather_db.get(city)
    if info:
        return json.dumps({
            "city": city,
            "temperature": f"{info['temp']}°C",
            "condition": info["condition"],
            "humidity": f"{info['humidity']}%"
        }, ensure_ascii=False)
    return json.dumps({"error": f"未找到城市 {city} 的天气数据"}, ensure_ascii=False)


def calculate(expression: str) -> str:
    """安全计算数学表达式"""
    allowed_chars = set("0123456789+-*/.() ")
    if not all(c in allowed_chars for c in expression):
        return json.dumps({"error": "表达式包含不允许的字符"}, ensure_ascii=False)
    try:
        result = eval(expression)
        return json.dumps({"expression": expression, "result": result}, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)


def search_knowledge(query: str) -> str:
    """模拟知识库搜索"""
    knowledge = {
        "python": "Python 是一种解释型、面向对象的高级编程语言，由 Guido van Rossum 于 1991 年创建。",
        "langchain": "LangChain 是一个用于开发大语言模型应用的开源框架，支持链式调用、RAG、Agent 等。",
        "qwen": "通义千问 (Qwen) 是阿里云推出的大语言模型系列，支持文本、图像、代码等多模态任务。",
    }
    for key, value in knowledge.items():
        if key in query.lower():
            return json.dumps({"query": query, "result": value}, ensure_ascii=False)
    return json.dumps({"query": query, "result": "未找到相关信息"}, ensure_ascii=False)


# ============================================================
# 第二步：定义 Tools Schema（告诉模型有哪些技能可用）
# ============================================================

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取指定城市的天气信息，包括温度、天气状况、湿度",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称，如：北京、上海、深圳"
                    }
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "计算数学表达式，支持加减乘除和括号",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "数学表达式，如：(10 + 5) * 3"
                    }
                },
                "required": ["expression"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_knowledge",
            "description": "搜索知识库，查询技术概念和术语的解释",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "搜索关键词或问题"
                    }
                },
                "required": ["query"]
            }
        }
    }
]

# 函数名到实际函数的映射
SKILL_MAP = {
    "get_weather": get_weather,
    "calculate": calculate,
    "search_knowledge": search_knowledge,
}


# ============================================================
# 第三步：Agent 执行循环
# ============================================================

def run_agent(user_input: str, verbose: bool = True):
    """
    Agent 执行流程：
    1. 用户提问
    2. 模型判断是否需要调用工具
    3. 如果需要 → 调用对应函数 → 将结果返回给模型
    4. 模型生成最终回答
    """
    if verbose:
        print(f"\n{'='*50}")
        print(f"用户: {user_input}")
        print(f"{'='*50}")

    messages = [
        {
            "role": "system",
            "content": (
                "你是一个智能助手，拥有以下技能：查询天气、数学计算、知识库搜索。"
                "根据用户的问题，自主判断是否需要使用工具，以及使用哪个工具。"
                "可以同时调用多个工具来回答复杂问题。"
            )
        },
        {"role": "user", "content": user_input}
    ]

    # 第一次请求：让模型决定是否调用工具
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=TOOLS,
        tool_choice="auto",  # auto: 模型自行决定 | required: 强制调用
    )

    assistant_message = response.choices[0].message

    # 如果模型不需要调用工具，直接返回
    if not assistant_message.tool_calls:
        if verbose:
            print(f"\n[模型直接回答，未调用工具]")
            print(f"回答: {assistant_message.content}")
        return assistant_message.content

    # 模型要求调用工具
    messages.append(assistant_message)

    if verbose:
        print(f"\n[模型决定调用 {len(assistant_message.tool_calls)} 个工具]")

    # 执行每个工具调用
    for tool_call in assistant_message.tool_calls:
        func_name = tool_call.function.name
        func_args = json.loads(tool_call.function.arguments)

        if verbose:
            print(f"  -> 调用: {func_name}({func_args})")

        # 执行对应的 Python 函数
        func = SKILL_MAP.get(func_name)
        if func:
            result = func(**func_args)
        else:
            result = json.dumps({"error": f"未知工具: {func_name}"})

        if verbose:
            print(f"     结果: {result}")

        # 将工具执行结果追加到消息中
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": result,
        })

    # 第二次请求：让模型根据工具结果生成最终回答
    final_response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
    )

    final_answer = final_response.choices[0].message.content

    if verbose:
        print(f"\n最终回答: {final_answer}")

    return final_answer


# ============================================================
# 第四步：多轮 Agent 对话
# ============================================================

def agent_chat():
    """交互式 Agent 对话，支持多轮"""
    print("=== Agent Skills 交互模式 (输入 quit 退出) ===")
    print("可用技能: 天气查询 | 数学计算 | 知识搜索\n")

    while True:
        user_input = input("你: ").strip()
        if not user_input:
            continue
        if user_input.lower() == "quit":
            print("再见！")
            break
        run_agent(user_input)


# ============================================================
# 运行示例
# ============================================================

def run_examples():
    """运行预设的示例，展示不同场景"""
    examples = [
        # 单工具调用
        "北京今天天气怎么样？",
        # 数学计算
        "帮我算一下 (15 + 25) * 3 - 10 等于多少",
        # 知识查询
        "什么是 LangChain？",
        # 多工具调用（模型可能一次调用多个）
        "上海和深圳的天气分别是什么？哪个更热？",
        # 混合场景
        "北京气温多少度？如果升高5度再乘以2是多少？",
        # 不需要工具的问题
        "你好，请做个自我介绍",
    ]

    for question in examples:
        run_agent(question)
        print()


if __name__ == "__main__":
    print("请选择模式:")
    print("1. 运行预设示例")
    print("2. 交互式 Agent 对话")

    choice = input("选择 (1/2): ").strip()
    if choice == "1":
        run_examples()
    elif choice == "2":
        agent_chat()
    else:
        print("无效选项")
