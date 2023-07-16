from app.pipelines.entities.loaders import Loader
from app.data.services import BaseDataSource
from app.agents.entities.query_router import AgentQueryRouter

from typing import Dict, List, Type

import inspect
import importlib.util


def extract_classes_from_file(config: Dict[str, str]) -> Dict[str, Type]:
    classes = {}
    file_path = config['data_sources_path']
    # Load the module from the file
    spec = importlib.util.spec_from_file_location("module_name", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # Inspect the module to find classes
    for name, obj in inspect.getmembers(module):
        if inspect.isclass(obj) and issubclass(obj, BaseDataSource) and obj != BaseDataSource:
            classes[name] = obj

    return classes


def update_pipeline(config: Dict[str, str]) -> List[str]:

    loader = Loader(config)

    class_mapper = extract_classes_from_file(config)
    index_name = config['index_name']

    new_documents, updated_data_sources = [], []

    loader.upload()

    indexed_datasets = loader.get_attribute_from_index('name')

    for name, data_source in class_mapper.items():

        data_source_instance = data_source()

        data_source_metadata = data_source_instance.update(indexed_datasets)

        if not data_source_metadata: continue

        data_source_documents = data_source.get_documents_from_metadata(data_source_metadata)

        new_documents.extend(data_source_documents)
        updated_data_sources.append(name)

    if not new_documents: return []
    new_index = loader.get_embeddings(new_documents)

    loader.update_index(new_index)

    loader.save_index(index_name)

    return updated_data_sources


def query_pipeline(query: str, config: Dict) -> str:

    loader = Loader(config)

    db = loader.upload()

    docs = db.similarity_search(query, **config['index']['search_kwargs'])

    class_mapper = extract_classes_from_file(config)

    docs_class_mapper = {document.metadata['url']: class_mapper[document.metadata['data_source']]() for document in docs}

    agent = AgentQueryRouter(docs_class_mapper, config)

    return agent(query=query)
    





