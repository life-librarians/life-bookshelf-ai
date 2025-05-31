import os
import pickle
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_path = os.path.join(BASE_DIR, 'data', 'split_documents.pkl')
csv_path = os.path.join(BASE_DIR, 'data', 'dummy_questions.csv')

def load_and_split(csv_path):
    loader = CSVLoader(
        file_path=csv_path,
        source_column='question',
        encoding='utf-8-sig',
    )
    documents = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
    return splitter.split_documents(documents)

def ensure_split_documents():
    if not os.path.exists(file_path):
        print("split_documents.pkl이 존재하지 않아 생성합니다...")
        split_docs = load_and_split(csv_path)
        with open(file_path, 'wb') as f:
            pickle.dump(split_docs, f)
        print("split_documents.pkl 생성 완료!")
    else:
        print("split_documents.pkl이 이미 존재합니다.")

if __name__ == "__main__":
    ensure_split_documents()