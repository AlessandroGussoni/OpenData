from pydantic import BaseModel
from typing import List

class MetaData(BaseModel):

    text: List[str] = []
    url: List[str] = []
    name: List[str] = []
    data_source: List[str] = []
