import sys
import os

# Get the current directory of the main.py file
current_dir = os.path.dirname(os.path.abspath(__file__))
# get parent dir
parent_dir = os.path.dirname(current_dir)
# Add the parent directory to the Python path for the whole project
sys.path.append(parent_dir)

from app.data.services.datasources import BaseDataSource, IAbstractDataSource

from app.pipelines.services.executors import update_pipeline, extract_classes_from_file
from app.pipelines.entities.loaders import config_loader

config = config_loader()

updated_data_sources = update_pipeline(config)