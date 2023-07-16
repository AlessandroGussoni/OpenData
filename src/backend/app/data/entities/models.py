from pydantic import BaseModel
from typing import List

class MetaData(BaseModel):

    dataset_id: List[str] = []
    text: List[str] = []
    url: List[str] = []
    name: List[str] = []
    data_source: List[str] = []

class QueryModel(BaseModel):
    query: str