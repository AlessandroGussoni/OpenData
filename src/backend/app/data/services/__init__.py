from abc import ABC, abstractmethod
from typing import List, Union, Type

from pandas import DataFrame

from data.entities.models import MetaData
from pydantic import BaseModel

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
    def read_datasets(self, 
                      dataset_names: Union[List[str], str], 
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

    def __init__(self, 
                 name: str,
                 url: str) -> None:
        self.name = name
        self.url = url


    def __repr__(self) -> str:
        return self.name

    def update(self) -> bool:
        
        """
        Method used to keep the index updated
        """

        # get all datasets available on datasource
        available_datasets = self._list_available_datasets()
        # get dataset already scraped
        indexed_datasets = self._upload()
        # get datasets to be scraped
        new_datasets = list(set(available_datasets).difference(set(indexed_datasets)))
        # if new ds found, run scraping pipeline
        if new_datasets:
            # get new ds metadata
            metadata = self._get_metadata(new_datasets)
            # save metadata
            self.save(metadata)
            return True
        # if not updated return false
        return False

    
    def save(self, 
             old_metadata, 
             new_metadata):
        return 
    
    def _upload(self):
        return