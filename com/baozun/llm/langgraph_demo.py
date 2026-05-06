"""
LangGraph 入门示例：智能分类问答 Agent
========================================
演示 LangGraph 核心概念：State、Node、Edge、Conditional Edge

流程图：
    [开始] → [分类器] →（数学问题）→ [计算节点] → [回答节点] → [结束]
                      →（知识问题）→ [检索节点] → [回答节点] → [结束]
                      →（闲聊）  → [回答节点] → [结束]

依赖安装 (需要 Python >= 3.9):
    pip install langgraph langchain-openai
"""
import os
from typing import TypedDict, Literal

from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

# ============================================================
# 配置
# ============================================================

API_KEY = os.getenv("DASHSCOPE_API_KEY", "sk-b82c2c1929d1414eb808d988d0f3f72c")
BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
MODEL = "qwen-plus"


def create_llm():
    return ChatOpenAI(
        model=MODEL,
        api_key=API_KEY,
        base_url=BASE_URL,
        temperature=0.3,
    )


# ============================================================
# 第一步：定义 State（状态）
# ============================================================
# State 是在图的所有节点之间共享的数据结构
# 每个节点可以读取和更新 State

class AgentState(TypedDict):
    """Agent 的状态定义"""
    question: str           # 用户输入的问题
    category: str           # 问题分类：math / knowledge / chat
    context: str            # 中间处理结果（检索或计算的内容）
    answer: str             # 最终回答


# ============================================================
# 第二步：定义 Node（节点）
# ============================================================
# 每个节点是一个函数，接收 State，返回更新后的部分 State

def classify_node(state: AgentState) -> dict:
    """
    分类节点：判断用户问题的类型
    """
    llm = create_llm()
    messages = [
        SystemMessage(content=(
            "你是一个问题分类器。根据用户的问题，返回以下分类之一：\n"
            "- math: 数学计算类问题\n"
            "- knowledge: 知识问答类问题\n"
            "- chat: 日常闲聊\n\n"
            "只返回分类标签，不要返回其他内容。"
        )),
        HumanMessage(content=state["question"]),
    ]
    response = llm.invoke(messages)
    category = response.content.strip().lower()

    # 确保分类有效
    if category not in ("math", "knowledge", "chat"):
        category = "chat"

    print(f"  [分类器] 问题类型: {category}")
    return {"category": category}


def math_node(state: AgentState) -> dict:
    """
    计算节点：处理数学问题
    """
    llm = create_llm()
    messages = [
        SystemMessage(content=(
            "你是一个数学计算助手。请解答用户的数学问题，给出详细的计算步骤。"
        )),
        HumanMessage(content=state["question"]),
    ]
    response = llm.invoke(messages)
    print(f"  [计算节点] 已完成数学计算")
    return {"context": response.content}


def knowledge_node(state: AgentState) -> dict:
    """
    检索节点：处理知识类问题
    （这里用 LLM 模拟检索，实际项目中可接入向量数据库）
    """
    llm = create_llm()
    messages = [
        SystemMessage(content=(
            "你是一个知识库助手。请根据你的知识回答用户的问题，"
            "给出准确、有条理的信息。"
        )),
        HumanMessage(content=state["question"]),
    ]
    response = llm.invoke(messages)
    print(f"  [知识节点] 已检索相关知识")
    return {"context": response.content}


def answer_node(state: AgentState) -> dict:
    """
    回答节点：整合信息，生成最终回答
    """
    # 如果是闲聊，直接让 LLM 回答
    if state["category"] == "chat":
        llm = create_llm()
        messages = [
            SystemMessage(content="你是一个友好的聊天助手，用轻松的语气回答。"),
            HumanMessage(content=state["question"]),
        ]
        response = llm.invoke(messages)
        answer = response.content
    else:
        # 数学或知识类，使用中间结果
        answer = state.get("context", "抱歉，我无法回答这个问题。")

    print(f"  [回答节点] 已生成最终回答")
    return {"answer": answer}


# ============================================================
# 第三步：定义条件边（路由逻辑）
# ============================================================

def route_by_category(state: AgentState) -> Literal["math", "knowledge", "chat"]:
    """
    根据分类结果，决定下一步走哪个节点
    这就是 Conditional Edge 的核心：动态路由
    """
    return state["category"]


# ============================================================
# 第四步：构建 Graph（图）
# ============================================================

def build_graph():
    """构建 LangGraph 工作流"""

    # 1. 创建图，指定 State 类型
    graph = StateGraph(AgentState)

    # 2. 添加节点
    graph.add_node("classify", classify_node)
    graph.add_node("math", math_node)
    graph.add_node("knowledge", knowledge_node)
    graph.add_node("answer", answer_node)

    # 3. 设置入口节点
    graph.set_entry_point("classify")

    # 4. 添加条件边：分类节点 → 根据结果路由到不同节点
    graph.add_conditional_edges(
        "classify",             # 源节点
        route_by_category,      # 路由函数
        {                       # 路由映射
            "math": "math",
            "knowledge": "knowledge",
            "chat": "answer",   # 闲聊直接到回答节点
        }
    )

    # 5. 添加普通边：处理节点 → 回答节点
    graph.add_edge("math", "answer")
    graph.add_edge("knowledge", "answer")

    # 6. 添加终止边：回答节点 → 结束
    graph.add_edge("answer", END)

    # 7. 编译图
    app = graph.compile()
    return app


# ============================================================
# 运行
# ============================================================

if __name__ == "__main__":
    print("=" * 50)
    print("  LangGraph 智能分类问答 Agent")
    print("=" * 50)
    print()
    print("流程: 问题 → 分类 → 对应处理节点 → 生成回答")
    print("输入 quit 退出")
    print()

    # 构建图
    app = build_graph()

    # 用几个示例问题演示
    demo_questions = [
        "计算 (15 + 27) * 3 - 18 的结果",
        "什么是量子计算？",
        "今天天气真好啊",
    ]

    print("-" * 50)
    print("演示模式：自动运行 3 个示例问题")
    print("-" * 50)

    for q in demo_questions:
        print(f"\n问题: {q}")
        print(f"{'─' * 40}")

        # 调用图：传入初始 State
        result = app.invoke({
            "question": q,
            "category": "",
            "context": "",
            "answer": "",
        })

        print(f"\n回答: {result['answer']}")
        print(f"{'═' * 50}")

    # 交互模式
    print("\n\n进入交互模式：")
    print("-" * 50)

    while True:
        question = input("\n你的问题: ").strip()
        if not question:
            continue
        if question.lower() == "quit":
            print("再见！")
            break

        result = app.invoke({
            "question": question,
            "category": "",
            "context": "",
            "answer": "",
        })

        print(f"\n回答: {result['answer']}")
        print(f"{'─' * 50}")
