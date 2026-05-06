"""
RAG (Retrieval-Augmented Generation) 完整示例
=============================================
使用 LangChain + FAISS + Qwen 实现基于本地文件的知识库问答。

依赖安装:
    pip install langchain langchain-community langchain-openai faiss-cpu

支持读取的文件格式: .txt, .md
"""
import os
from typing import List
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.documents import Document


# ============================================================
# 配置
# ============================================================

API_KEY = os.getenv("DASHSCOPE_API_KEY", "sk-b82c2c1929d1414eb808d988d0f3f72c")
BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
MODEL = "qwen-plus"
EMBEDDING_MODEL = "text-embedding-v3"


def create_llm():
    """创建 LLM 实例"""
    return ChatOpenAI(
        model=MODEL,
        api_key=API_KEY,
        base_url=BASE_URL,
        temperature=0.3,
    )


def create_embeddings():
    """创建 Embedding 实例"""
    return OpenAIEmbeddings(
        model=EMBEDDING_MODEL,
        api_key=API_KEY,
        base_url=BASE_URL,
        check_embedding_ctx_length=False,
    )


# ============================================================
# 第一步：加载本地文档
# ============================================================

def load_documents(file_path: str) -> List[Document]:
    """
    从本地文件或目录加载文档。

    Args:
        file_path: 文件路径或目录路径
                   - 文件: 直接加载该文件
                   - 目录: 加载目录下所有 .txt 和 .md 文件

    Returns:
        Document 列表
    """
    documents = []
    supported_ext = {".txt", ".md"}

    if os.path.isfile(file_path):
        files = [file_path]
    elif os.path.isdir(file_path):
        files = [
            os.path.join(file_path, f)
            for f in os.listdir(file_path)
            if os.path.splitext(f)[1].lower() in supported_ext
        ]
    else:
        raise FileNotFoundError(f"路径不存在: {file_path}")

    for fp in sorted(files):
        ext = os.path.splitext(fp)[1].lower()
        if ext not in supported_ext:
            continue
        with open(fp, "r", encoding="utf-8") as f:
            content = f.read()
        if content.strip():
            documents.append(Document(
                page_content=content,
                metadata={"source": fp}
            ))
            print(f"  已加载: {fp} ({len(content)} 字符)")

    if not documents:
        raise ValueError(f"未找到有效文档: {file_path}")

    print(f"  共加载 {len(documents)} 个文档\n")
    return documents


# ============================================================
# 第二步：文档分割 + 向量化 + 构建向量数据库
# ============================================================

def build_vector_store(documents: List[Document], chunk_size: int = 500, chunk_overlap: int = 50):
    """
    将文档分割为小段并构建 FAISS 向量数据库。

    Args:
        documents: Document 列表
        chunk_size: 每个分割块的最大字符数
        chunk_overlap: 相邻块之间的重叠字符数

    Returns:
        FAISS 向量数据库实例
    """
    print("[构建向量数据库]")

    # 分割文档
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", "。", "！", "？", ".", " ", ""]
    )
    chunks = splitter.split_documents(documents)
    print(f"  文档被分割为 {len(chunks)} 个片段")

    # 向量化并存入 FAISS
    embeddings = create_embeddings()
    vector_store = FAISS.from_documents(chunks, embeddings)
    print(f"  向量数据库构建完成\n")

    return vector_store


# ============================================================
# 第三步：构建 RAG 问答链
# ============================================================

def build_rag_chain(vector_store, top_k: int = 3):
    """
    构建 RAG 问答链。

    Args:
        vector_store: FAISS 向量数据库
        top_k: 检索返回的文档数量

    Returns:
        可执行的 RAG 链
    """
    llm = create_llm()
    retriever = vector_store.as_retriever(search_kwargs={"k": top_k})

    # 定义回答的 Prompt
    prompt = ChatPromptTemplate.from_template(
        """你是一个知识库问答助手。请根据以下检索到的文档内容回答用户问题。

规则：
1. 只根据提供的文档内容回答，不要编造信息
2. 如果文档中没有相关信息，请明确告知用户
3. 回答时引用信息来源（文件名）

检索到的文档：
{context}

用户问题：{input}

回答："""
    )

    # 组装链
    document_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, document_chain)

    return rag_chain


# ============================================================
# 第四步：执行问答
# ============================================================

def ask(rag_chain, question: str, verbose: bool = True) -> str:
    """
    向 RAG 链提问。

    Args:
        rag_chain: 构建好的 RAG 链
        question: 用户问题
        verbose: 是否打印检索到的文档

    Returns:
        回答文本
    """
    result = rag_chain.invoke({"input": question})

    if verbose:
        print(f"问题: {question}")
        print(f"{'─' * 40}")
        print(f"回答: {result['answer']}")
        print(f"{'─' * 40}")
        print(f"参考文档 ({len(result['context'])} 个片段):")
        for i, doc in enumerate(result['context'], 1):
            source = doc.metadata.get('source', '未知')
            preview = doc.page_content[:80].replace('\n', ' ')
            print(f"  [{i}] {source}")
            print(f"      \"{preview}...\"")
        print()

    return result['answer']


# ============================================================
# 完整流程：一键运行
# ============================================================

def rag_pipeline(file_path: str):
    """
    RAG 完整流程：加载文档 → 构建向量库 → 交互式问答

    Args:
        file_path: 文件或目录路径
    """
    # 1. 加载文档
    print("[加载文档]")
    documents = load_documents(file_path)

    # 2. 构建向量数据库
    vector_store = build_vector_store(documents)

    # 3. 构建 RAG 链
    print("[构建 RAG 问答链]")
    rag_chain = build_rag_chain(vector_store)
    print("  就绪！\n")

    # 4. 交互式问答
    print("=" * 50)
    print("  RAG 知识库问答 (输入 quit 退出)")
    print("=" * 50)

    while True:
        question = input("\n你的问题: ").strip()
        if not question:
            continue
        if question.lower() == "quit":
            print("再见！")
            break
        print()
        ask(rag_chain, question)


# ============================================================
# 入口
# ============================================================

if __name__ == "__main__":
    print("=" * 50)
    print("  RAG 知识库问答系统")
    print("=" * 50)
    print()

    # 输入知识库路径
    default_path = r"D:\project\local-design\pythonProject\com\baozun\llm\knowledge"
    path = input(f"请输入知识库文件/目录路径\n(默认: {default_path}): ").strip()
    if not path:
        path = default_path

    print()
    rag_pipeline(path)
