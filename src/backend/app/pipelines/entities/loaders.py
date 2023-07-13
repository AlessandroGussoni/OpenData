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

    def __init__(self, config) -> None:
        self.config = config

    def get_attribute_from_index(self, attr) -> List[str]:
        if not self.db: return []
        return [document.metadata[attr] for document in self.db.docstore.__dict__['_dict'].values()]

    def get_embedding_class(self):
        embeddings_name = self.config['embeddings']['active']
        embeddings = globals()[embeddings_name](**self.config['embeddings'][embeddings_name])
        return embeddings
    
    def get_vector_db(self):
        db_name = self.config['index']['db_name']
        db = globals()[db_name]
        return db

    
    def upload(self) -> Union[Type, Type[None]]:
        vector_db = self.get_vector_db()
        embeddings = self.get_embedding_class()
        
        try:
            db = vector_db.load_local(self.config["index_name"], embeddings)

        except RuntimeError as e:
            db = None
        setattr(self, 'db', db)
        return db
            
    def get_embeddings(self, documents: List[Document]) -> None:

        vector_db = self.get_vector_db()
        embeddings = self.get_embedding_class()

        return vector_db.from_documents(documents, embeddings)
            
    def update_index(self,
                     new_metadata_index: Type) -> None:
        if not isinstance(self.db, type(None)):
            self.db.merge_from(new_metadata_index)
        else:
            self.db = new_metadata_index

    
    def save_index(self, 
                   name: str) -> None:
        self.db.save_local(name)

    def destroy_index(self, 
                      name: str):
        os.remove(name)