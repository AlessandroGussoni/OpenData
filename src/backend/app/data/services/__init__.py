from abc import ABC, abstractmethod
from typing import List, Dict, Union, Type

from urllib.request import urlopen
from pandas import DataFrame
import csv

from app.data.entities.models import MetaData

from langchain.docstore.document import Document

class IAbstractDataSource(ABC):

    @abstractmethod
    def _list_available_datasets(self, *args, **kwargs) -> List[str]:
        pass

    @abstractmethod
    def _get_metadata(self, 
                     dataset_names: Union[List[str], str],
                     *args, **kwargs):
        pass

    @abstractmethod
    def read_dataset(self, 
                     dataset_url: Union[List[str], str], 
                     *args, **kwargs) -> DataFrame:
        pass


class MetaDataMixIn(object):

    @staticmethod
    def _add_tags(title: str, notes: str, tags: List[str]) -> str:
        return title + '\n' + notes + "\nTag del Dataset: " + " ".join([tag for tag in tags])
    
    @staticmethod
    def _create_metadata() -> Type[MetaData]:
        return MetaData()
    
    @staticmethod
    def _update_metadata(metadata: Type[MetaData],
                         **kwargs) -> Type[MetaData]:
       for name, value in kwargs.items(): getattr(metadata, name).append(value)

       return metadata



class BaseDataSource(MetaDataMixIn):    

    """
    Possible refactor: Ogni classe al momento carica e salva l indice, 
    ha più senso che ogni ds aggiorni i metadata e l indice venga caricato una volta sola
    
    """

    def __init__(self, 
                 name: str,
                 url: str) -> None:
        self.name = name
        self.url = url


    def __repr__(self) -> str:
        return self.name
    
    @staticmethod
    def infer_separetor(url: str):
        
        data = urlopen(url)
        dialect = csv.Sniffer().sniff(data.readline().decode())
        return dialect.delimiter
    
    @staticmethod
    def get_documents_from_metadata(metadata: Dict[str, List[str]]) -> List[Document]:
        # logica oscena, devo cambiarla (velocizzarla per lo meno) 
        docs = [Document(page_content=row['text'], metadata={**row.to_dict()}) for i, row in DataFrame(metadata).iterrows()]
        return docs

    def update(self, 
               indexed_datasets: List) -> Union[None, Dict[str, List[str]]]:
        
        """
        Method used to keep the index updated
        """

        # get all datasets available on datasource
        available_datasets = self._list_available_datasets()
        # get datasets to be scraped
        new_datasets = list(set(available_datasets).difference(set(indexed_datasets)))
        # if new ds found, run scraping pipeline
        if new_datasets:
            # get new ds metadata
            metadata = self._get_metadata(new_datasets)
            
            return metadata
        return None
