import os
import json

from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.embeddings.fake import FakeEmbeddings
from langchain.docstore.document import Document

from typing import Union, List, Dict, Type

def config_loader() -> Dict:

    with open(r"src\backend\config.json", 'rb') as file:
        config = json.load(file)

    return config


class Loader(object):

    _EMBEDDINGS_MAP = {
        "fake": FakeEmbeddings,
        "openai": OpenAIEmbeddings
    }

    _DB_MAP = {
        "Faiss": FAISS
    }

    def __init__(self, config) -> None:
        self.config = config

    def get_names_from_index(self) -> List:
        if not self.index: return []
        return [document.metadata['name'] for document in self.index.docstore.__dict__['dict'].values()]

    def get_embedding_class(self):
        embeddings_name = self.config['embeddings']
        embeddings = Loader._EMBEDDINGS_MAP[embeddings_name]()
        return embeddings
    
    def get_vector_db(self):
        db_name = self.config['db_name']
        db = Loader._DB_MAP[db_name]
        return db

    
    def upload(self) -> Union[Type, Type[None]]:
        vector_db = self.get_vector_db()
        embeddings = self.get_embedding_class()
        
        try:
            db = vector_db.load_local(self.config["index_name"], embeddings)

        except FileNotFoundError as e:
            db = None
        setattr(self, 'db', db)
        return db
            
    def get_embeddings(self, documents: List[Document]) -> None:

        vector_db = self.loader.get_vector_db()
        embeddings = self.loader.get_embedding_class()

        return vector_db.from_documents(documents, embeddings)
            
    def update_index(self,
                     new_metadata_index: Type) -> None:
        
        self.index.merge_from(new_metadata_index)

    
    def save_index(self, 
                   name: str) -> None:
        self.index.save_local(name)

    def destroy_index(self, 
                      name: str):
        os.remove(name)