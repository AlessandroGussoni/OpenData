from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.embeddings.gpt4all import GPT4AllEmbeddings

import csv
import collections 

from dotenv import load_dotenv

load_dotenv()

db = FAISS.load_local("src/backend/database/docs_index", GPT4AllEmbeddings())

urls = [document.metadata['url'] for document in db.docstore.__dict__['_dict'].values()]


print([item for item, count in collections.Counter(urls).items() if count > 1])

print(len(set(urls)))