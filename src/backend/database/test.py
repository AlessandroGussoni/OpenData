from langchain.vectorstores import FAISS
from langchain.embeddings import FakeEmbeddings

new_db = FAISS.load_local("src/backend/database/docs_index", FakeEmbeddings(size=100))

names = [document.metadata['name'] for document in new_db.docstore.__dict__['_dict'].values()]

print(len(names))