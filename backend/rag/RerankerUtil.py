import os
from dotenv import load_dotenv
from FlagEmbedding import FlagReranker

load_dotenv()
reranker = None
def print_recall(docs):
    print("检索到的文档内容：")
    # 遍历docs获取每条检索到的文档信息
    for doc in docs[:5]:
        print(doc.page_content)
        print("-" * 20)
    return docs
def retriever_func(question,retriever):

    vector_result = retriever.invoke(question)
    print_recall(vector_result)
    # bm25
    # bm25, docs = BM25Util.build_bm25_index(vector_db)
    # bm25_result = BM25Util.bm25_search(bm25, question, docs, 10)
def reranker_func(data):
    print("开始进行重排序")
    global reranker
    if reranker is None:
        reranker = FlagReranker(
            model_name_or_path=os.getenv('RERANKER_MODEL_PATH'),  # 本地模型路径由 .env 配置（见 .env.example）
            use_fp16=True,
            devices=['cuda:0'],
        )
    question = data['question']
    contexts = data['context']
    history = data['history']
    reranker_input = [(question, doc.page_content) for doc in contexts]
    scores = reranker.compute_score(reranker_input)

    doc_scores = list(zip(contexts, scores))
    doc_scores = sorted(doc_scores, key=lambda x: x[1], reverse=True)

    sorted_scores = [dot for dot, score in doc_scores]
    return {
        "context": sorted_scores,
        "question": question,
        "history": history,
    }
