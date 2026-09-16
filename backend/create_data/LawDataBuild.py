from langchain_core.documents import Document
from langchain_chroma import Chroma
from ai import LoadEmbeddingModel
import json
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# 网络安全数据
data_file = Path(os.getenv('DATA_ROOT')) / 'cve_all.jsonl'
vector_db_path = os.getenv('CHROMA_PATH')
collection_name = os.getenv('COLLECTION_NAME')

# 读取 jsonl
# 每行一条 {page_content, metadata}
rows = []
with open(data_file, encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if line:
            rows.append(json.loads(line))

document = [Document(page_content=r['page_content'], metadata=r['metadata']) for r in rows]
print(f'共加载 {len(document)} 条文档')

try:
    Chroma.from_documents(
        documents=document,
        collection_name=collection_name,
        persist_directory=vector_db_path,
        embedding=LoadEmbeddingModel.load_embedding_model(),
        collection_metadata={"hnsw:space": 'cosine'},
    )
    print('传入成功')
except Exception as e:
    print(e)
