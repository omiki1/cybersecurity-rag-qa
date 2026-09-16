import jieba
from langchain_core.documents import Document
from rank_bm25 import BM25Okapi

from ai import LoadChroma

STOP_WORDS = {
    "的", "了", "在", "是", "我", "有", "和", "就", "不", "人", "都",
    "一", "一个", "上", "也", "很", "到", "说", "要", "去", "你", "会",
    "着", "没有", "看", "好", "自己", "这", "那", "他", "她", "它", "们",
    "这个", "那个", "什么", "哪", "怎么", "吗", "呢", "吧", "啊", "哦",
    "还", "被", "把", "让", "从", "对", "与", "但", "而", "或", "所",
    "为", "以", "及", "可", "可以", "能", "能够", "应该", "需要", "已经",
    "虽然", "如果", "因为", "所以", "只是", "还是", "不过", "然后",
    "之", "其", "中", "等", "等等", "即", "于", "由", "比", "除了",
    "关于", "以及", "并且", "此外", "另外", "过", "着", "来", "去",
    "做", "作", "像", "如", "如同", "由于",
}

def tokenize(text:str)->list:
    return [w for w in jieba.cut(text) if w.strip() and w.strip() not in STOP_WORDS]

def build_bm25_index(vector_db):
    data = vector_db.get()
    docs = []
    for i in range(len(data['ids'])):
        docs.append(Document(
            page_content=data['documents'][i],
            id=data['ids'][i],
            metadata={'source': data['metadatas'][i]},
        )
    )
    bm25 = BM25Okapi([tokenize(d) for d in data['documents']])
    return docs, bm25
_bm25 = None
_docs = None
def get_bm25_index(vector_db):
    global _bm25, _docs
    if _bm25 is None:
        _docs, _bm25 = build_bm25_index(vector_db)
    return _docs, _bm25
def search_bm25(bm25,question:str,docs:list,k:int=20):
    scores = bm25.get_scores(tokenize(question))
    top_idx = sorted(range(len(scores)), key=lambda x: scores[x], reverse=True)[:k]
    return [docs[i] for i in top_idx]
if __name__ == '__main__':
    vector_db = LoadChroma.load_chrome_conn()
    docs,bm25 = build_bm25_index(vector_db)
    result = search_bm25(bm25,"公安机关接到网络安全报案后应当做什么事情？", docs)
    print(result)