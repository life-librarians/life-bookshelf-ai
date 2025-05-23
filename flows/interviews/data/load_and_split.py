import os
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import pickle
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_path = os.path.join(BASE_DIR, 'data', 'split_documents.pkl')

def load_and_split(csv_path):
    loader = CSVLoader(
        file_path=csv_path,
        source_column='question',
        meta_columns=['topic_main', 'topic_sub', 'question_purpost', 'time_period', 'self_reflection_type']
    )
    documents = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
    return splitter.split_documents(documents)

if __name__ == "__main__":
    split_docs = load_and_split('flows/interviews/data/dummy_questions.csv')
    with open(file_path, 'wb') as f:
        pickle.dump(split_docs, f)