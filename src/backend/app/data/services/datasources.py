import requests
from pandas import DataFrame

from data import BaseDataSource, IAbstractDataSource


from typing import Union, List, Dict


class OpenDataSource(BaseDataSource, IAbstractDataSource):

    VERSIONS = [1, 2]


    def __init__(self) -> None:
        name = "OpenData1"
        url = "http://www.datiopen.it/SpodCkanApi/api/"
        super().__init__(name, url)

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
                      *args, **kwargs) -> Dict[str, List[str]]:
        
        metadata = OpenDataSource._create_metadata()
        for name in dataset_names:

            dataset_version = [name in version_names for version_names in self.dfs].index(True) + 1
            dataset_url = self.parse_url_from_version(dataset_version) + '/' + name

            try:
                data = requests.get(dataset_url).json()
                title = data['title']
                notes = data['notes']
                tags = data['tags']

                df_metadata = OpenDataSource.add_tags(title, notes, tags)

                for resourse in data['resources']:
    
                    if resourse['format'] == 'csv':
                        url = resourse['url']
                    else: 
                        print(resourse['url'])
                
                metadata = OpenDataSource._update_metadata(metadata)   
                
            except Exception as e:
                print(f"{name} : {e.text}")

            return metadata.to_dict()

    def read_datasets(self, 
                      dataset_names: Union[List[str], str], 
                      *args, **kwargs) -> DataFrame:
        pass