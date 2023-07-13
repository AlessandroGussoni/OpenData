from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
import csv
from dotenv import load_dotenv

load_dotenv()

db = FAISS.load_local("src/backend/database/docs_index", OpenAIEmbeddings())

urls = [document.metadata['url'] for document in db.docstore.__dict__['_dict'].values()]

print(urls)