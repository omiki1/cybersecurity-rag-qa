import os
from dotenv import load_dotenv
from langchain_chroma import Chroma
from ai import LoadEmbeddingModel

load_dotenv()
chroma_conn = None
def load():
    global chroma_conn
    if chroma_conn is None:
        chroma_conn = Chroma(
            collection_name=os.getenv('COLLECTION_NAME'),
            persist_directory=os.getenv('CHROMA_PATH'),
            embedding_function=LoadEmbeddingModel.load_embedding_model(),
        )
    return chroma_conn

def search(question: str, k: int = 20):
    retriever = load().as_retriever(search_kwargs={"k": k})
    return retriever.invoke(question)
