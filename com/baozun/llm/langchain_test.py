import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.messages import HumanMessage, AIMessage
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.chains import create_retrieval_chain, create_history_aware_retriever
from langchain.chains.combine_documents import create_stuff_documents_chain

# 加载环境变量
load_dotenv()


class LangChainDemo:
    def __init__(self):
        # 初始化模型
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.7,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        self.embeddings = OpenAIEmbeddings()

    # ==================== Demo 1: 基础链式调用 ====================
    def basic_chain_demo(self):
        """最基础的链：提示词 + 模型 + 解析器"""
        print("=== Demo 1: 基础链式调用 ===")

        # 创建提示词模板
        prompt = ChatPromptTemplate.from_messages([
            ("system", "你是一个专业的{role}，请用{language}回答。"),
            ("human", "{question}")
        ])

        # 构建链：提示词 -> 模型 -> 字符串解析
        chain = prompt | self.llm | StrOutputParser()

        # 执行
        result = chain.invoke({
            "role": "程序员导师",
            "language": "中文",
            "question": "什么是递归？"
        })
        print(f"回答: {result}\n")
        return result

    # ==================== Demo 2: 带历史记录的对话链 ====================
    def conversation_with_memory(self):
        """带记忆功能的对话"""
        print("=== Demo 2: 带历史记录的对话 ===")

        # 对话历史
        history = []

        prompt = ChatPromptTemplate.from_messages([
            ("system", "你是一个 helpful 的助手。记住之前的对话内容。"),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}")
        ])

        chain = prompt | self.llm | StrOutputParser()

        # 第一轮对话
        history.append(HumanMessage(content="我叫张三"))
        response1 = chain.invoke({"history": history, "input": "我叫张三"})
        history.append(AIMessage(content=response1))
        print(f"AI: {response1}")

        # 第二轮对话（应该能记住名字）
        history.append(HumanMessage(content="我叫什么名字？"))
        response2 = chain.invoke({"history": history, "input": "我叫什么名字？"})
        print(f"AI: {response2}\n")

        return history

    # ==================== Demo 3: RAG 检索增强生成 ====================
    def rag_demo(self):
        """RAG：从文档中检索信息并回答"""
        print("=== Demo 3: RAG 检索增强生成 ===")

        # 模拟知识库文档
        documents = [
            "LangChain 是一个用于开发大语言模型应用的框架。",
            "LangChain 提供了链式调用、记忆、工具使用等组件。",
            "RAG (Retrieval-Augmented Generation) 结合检索和生成。",
            "向量数据库用于存储文档的嵌入向量，支持语义搜索。",
            "OpenAI 提供了 GPT 系列模型和 Embedding API。"
        ]

        # 文本分割
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=100,
            chunk_overlap=20
        )
        splits = text_splitter.create_documents(documents)

        # 创建向量数据库
        vectorstore = FAISS.from_documents(splits, self.embeddings)
        retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

        # 创建 RAG 链
        template = """基于以下上下文回答问题：
        {context}

        问题：{input}
        """
        prompt = ChatPromptTemplate.from_template(template)

        # 文档处理链
        document_chain = create_stuff_documents_chain(self.llm, prompt)

        # 检索链
        retrieval_chain = create_retrieval_chain(retriever, document_chain)

        # 查询
        result = retrieval_chain.invoke({"input": "什么是 LangChain？"})
        print(f"回答: {result['answer']}")
        print(f"检索到的文档: {[doc.page_content for doc in result['context']]}\n")

        return result

    # ==================== Demo 4: 工具调用 (Agent) ====================
    def agent_demo(self):
        """使用工具的智能体"""
        print("=== Demo 4: 工具调用 (Agent) ===")

        from langchain.agents import create_tool_calling_agent, AgentExecutor
        from langchain_core.tools import tool

        # 定义工具
        @tool
        def calculate(expression: str) -> str:
            """计算数学表达式"""
            try:
                return str(eval(expression))
            except:
                return "计算错误"

        @tool
        def search_weather(city: str) -> str:
            """查询城市天气（模拟）"""
            weather_db = {
                "北京": "晴天，25°C",
                "上海": "多云，28°C",
                "深圳": "小雨，30°C"
            }
            return weather_db.get(city, "未知城市")

        tools = [calculate, search_weather]

        # 创建 Agent
        prompt = ChatPromptTemplate.from_messages([
            ("system", "你是一个有用的助手，可以使用工具完成任务。"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])

        agent = create_tool_calling_agent(self.llm, tools, prompt)
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

        # 执行任务
        result = agent_executor.invoke({
            "input": "北京天气怎么样？然后计算 25 * 4 + 10 等于多少？"
        })
        print(f"最终结果: {result['output']}\n")

        return result

    # ==================== Demo 5: 结构化输出 ====================
    def structured_output_demo(self):
        """输出结构化数据（JSON）"""
        print("=== Demo 5: 结构化输出 ===")

        from pydantic import BaseModel, Field
        from langchain_core.output_parsers import JsonOutputParser

        # 定义输出结构
        class Movie(BaseModel):
            name: str = Field(description="电影名称")
            director: str = Field(description="导演")
            year: int = Field(description="上映年份")
            rating: float = Field(description="评分 0-10")
            genres: list[str] = Field(description="类型列表")

        parser = JsonOutputParser(pydantic_object=Movie)

        prompt = ChatPromptTemplate.from_template(
            """推荐一部经典电影，以JSON格式输出，包含以下字段：
            name, director, year, rating, genres

            {format_instructions}
            """
        ).partial(format_instructions=parser.get_format_instructions())

        chain = prompt | self.llm | parser

        result = chain.invoke({})
        print(f"结构化输出: {result}\n")
        return result

    # ==================== Demo 6: LCEL 复杂链 ====================
    def lcel_advanced_demo(self):
        """LCEL (LangChain Expression Language) 高级用法"""
        print("=== Demo 6: LCEL 复杂链 ===")

        # 并行处理 + 合并结果
        from langchain_core.runnables import RunnableParallel, RunnableLambda

        # 定义两个并行的处理分支
        def analyze_sentiment(text: str) -> str:
            prompt = ChatPromptTemplate.from_template(
                "分析以下文本的情感（正面/负面/中性）：{text}"
            )
            chain = prompt | self.llm | StrOutputParser()
            return chain.invoke({"text": text})

        def extract_keywords(text: str) -> str:
            prompt = ChatPromptTemplate.from_template(
                "从以下文本中提取3个关键词：{text}"
            )
            chain = prompt | self.llm | StrOutputParser()
            return chain.invoke({"text": text})

        # 构建并行链
        parallel_chain = RunnableParallel(
            sentiment=RunnableLambda(analyze_sentiment),
            keywords=RunnableLambda(extract_keywords),
            original=RunnablePassthrough()
        )

        text = "LangChain 真的太棒了，让开发AI应用变得简单！"
        result = parallel_chain.invoke(text)
        print(f"原文: {result['original']}")
        print(f"情感分析: {result['sentiment']}")
        print(f"关键词: {result['keywords']}\n")

        return result


# ==================== 运行所有 Demo ====================
def main():
    # 设置 API Key（或使用 .env 文件）
    os.environ["OPENAI_API_KEY"] = "sk-b82c2c1929d1414eb808d988d0f3f72c"

    demo = LangChainDemo()

    try:
        demo.basic_chain_demo()
        demo.conversation_with_memory()
        demo.rag_demo()
        demo.agent_demo()
        demo.structured_output_demo()
        demo.lcel_advanced_demo()
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()