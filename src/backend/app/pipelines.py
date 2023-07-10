import ast

from data.services.datasources import OpenDataSource

from typing import Dict, Type

def extract_classes_from_file(file_path: str) -> Dict[str, Type]:

    with open(file_path, 'r') as file:
        file_contents = file.read()

    tree = ast.parse(file_contents)

    class_map = {node.name: globals()[node.name]()for node in ast.walk(tree) if isinstance(node, ast.ClassDef)}

    return class_map


def update_pipeline(config: Dict[str, str]) -> Dict[str, bool]:

    class_mapper = extract_classes_from_file(config['data_sources_path'])

    update_check = {}

    for name, data_source in class_mapper.items():

        data_source_instance = data_source()

        update_check[name] = data_source_instance.update()

    return update_check
