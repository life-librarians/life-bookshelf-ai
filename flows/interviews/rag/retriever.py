import os
import pickle
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_path = os.path.join(BASE_DIR, 'data', 'split_documents.pkl')

with open(file_path, 'rb') as f:
    split_documents = pickle.load(f)

api_key = os.environ.get("AZURE_OPENAI_API_KEY")
embeddings = OpenAIEmbeddings(api_key=api_key)
vectorstore = FAISS.from_documents(documents=split_documents, embedding=embeddings)
vectorstore.save_local("data/faiss_index")

# 검색기(Retriever) 생성
vectorstore = FAISS.load_local(
    "data/faiss_index", 
    OpenAIEmbeddings(),
    allow_dangerous_deserialization=True
    )
retriever = vectorstore.as_retriever()

# To-do : 필요하면 역할을 더 세부적으로 분리

def get_retriever():
    return retriever