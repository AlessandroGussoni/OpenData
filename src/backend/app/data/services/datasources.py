import requests
from urllib.request import urlopen

from pandas import DataFrame, read_csv

from app.data.services import BaseDataSource, IAbstractDataSource

from typing import Union, List, Dict, Tuple


class OpenDataSource(BaseDataSource, IAbstractDataSource):

    VERSIONS = [1, 2]


    def __init__(self) -> None:
        name = "OpenData1"
        url = "http://www.datiopen.it/SpodCkanApi/api/"
        super().__init__(name, url)

    @staticmethod
    def parse_format_from_data(data: Dict) -> Union[str, None]:
        url = data.get('url', None)
        if not url: return url
        format_ = data['url'].split('.')[-1]
        return format_
    

    @staticmethod
    def parse_data_from_url(data_url: str) -> Tuple[str, str, str]:
        
        try:
            data = requests.get(data_url).json()
            title = data['title']
            notes = data['notes']
            tags = data['tags']
        except Exception as e:
            print(f"Level 1: {e} : {url}")
            return '', '', ''
        
        df_metadata = OpenDataSource._add_tags(title, notes, tags)      

        if "resources" in data.keys(): 
            list_info = data['resources']
        elif "relations" in data.keys(): 
            list_info = data['relations']
        else:
            print(f"{data_url} not found valid data key") 
            return '', '', ''

        url = ''
        for resource in list_info:
            format_ = OpenDataSource.parse_format_from_data(resource)
            if format_ == 'csv':
                url = resource['url']

        return url, title, df_metadata


    def parse_url_from_version(self, version: Union[int, str]) -> str:
        return self.url + f"{version}/rest/dataset"
    
    def _list_available_datasets(self, *args, **kwargs) -> List[str]:
        # get alla avilable datasets names
        nested_datasets = [requests.get(self.parse_url_from_version(version)).json() for version in OpenDataSource.VERSIONS]
        # save version to datasets
        setattr(self, 'dfs', nested_datasets)
        # flatten the list
        datasets_names = [item for sublist in nested_datasets for item in sublist]

        return datasets_names


    def _get_metadata(self, 
                      dataset_names: Union[List[str], str],
                      data_source_name: str,
                      *args, **kwargs) -> Dict[str, List[str]]:
        
        metadata = OpenDataSource._create_metadata()
        for name in dataset_names[:50]:

            dataset_version = [name in version_names for version_names in self.dfs].index(True) + 1
            dataset_url = self.parse_url_from_version(dataset_version) + '/' + name

            url, title, df_metadata = OpenDataSource.parse_data_from_url(dataset_url)

            if (url == '') and (title == '') and (df_metadata == ''): continue 
                
            metadata = OpenDataSource._update_metadata(metadata, 
                                                       url=url,
                                                       name=title,
                                                       text=df_metadata,
                                                       data_source=data_source_name)            
            print(f"{name} downloaded")
            

        return metadata.dict()


    def read_dataset(self, 
                     dataset_url: Union[List[str], str], 
                     *args, **kwargs) -> DataFrame:
        
        separator = BaseDataSource.infer_separetor(dataset_url)
        
        return read_csv(dataset_url, sep=separator, encoding='unicode_escape')