import sys
import os

# Get the current directory of the main.py file
current_dir = os.path.dirname(os.path.abspath(__file__))
# get parent dir
parent_dir = os.path.dirname(current_dir)
parent_dir2 = os.path.dirname(parent_dir)
parent_dir3 = os.path.dirname(parent_dir2)
# Add the parent directory to the Python path for the whole project
sys.path.append(parent_dir)
sys.path.append(parent_dir2)
sys.path.append(parent_dir3)
print(sys.path)

from services import executors
from entities import loaders

config = loaders.config_loader()
output = executors.update_pipeline(config)