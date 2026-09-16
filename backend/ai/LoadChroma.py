from langchain_chroma import Chroma
import os
from dotenv import load_dotenv
load_dotenv()
from ai import LoadEmbeddingModel


def load_chrome_conn():

    return Chroma(
        collection_name=os.getenv('COLLECTION_NAME'),
        persist_directory=os.getenv('CHROMA_PATH'),
        embedding_function=LoadEmbeddingModel.load_embedding_model(),
    )
