import sys
import os

# Get the current directory of the main.py file
current_dir = os.path.dirname(os.path.abspath(__file__))
# get parent dir
parent_dir = os.path.dirname(current_dir)
# Add the parent directory to the Python path for the whole project
sys.path.append(parent_dir)


from fastapi import FastAPI, Request
from contextlib import asynccontextmanager

from fastapi.openapi.docs import get_swagger_ui_html

from app.data.entities.models import QueryModel
from app.pipelines.services.executors import extract_classes_from_file, update_pipeline, query_pipeline
from app.pipelines.entities.loaders import config_loader, Loader
from fastapi.middleware.cors import CORSMiddleware

import uvicorn
from typing import List, Dict

from dotenv import load_dotenv


"""

Singleton (nel coolpkg)
O Depends()
"""

# TODO: Type Hint, Debugging endpoint, comments, add router
# TODO: Return docs if conversation is not resetted (make query endpoint stateful)
# TODO: maaaaaaybe passe the loader to the middleware
# TODO: key injection
# TODO: change config logic: i dont want to switch kwargs every time i switch llm



# Load the environment variables from the .env file
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    ''' Run at startup
        Initialise the Client and add it to app.state
    '''
    app.state.CONFIG = config_loader()
    yield


app = FastAPI(lifespan=lifespan)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/docs")
def read_docs():
    return get_swagger_ui_html(openapi_url="/openapi.json")

@app.get("/status",
         summary="Check if app is running")
def get_status(request: Request) -> Dict[str, bool]:
    return {"status": True}


@app.get("/list_datasources",
         summary="List all available data sources")
def list_data_sources(request: Request) -> Dict[str, List[str]]:

    class_mapper = extract_classes_from_file(request.app.state.CONFIG)

    names = list(class_mapper.keys())

    return {"names": names}


@app.get('/update_datasources',
         summary="Run the update ds pipeline")
def update_data_sources(request: Request) -> Dict[str, List[str]]:

    updated_data_sources = update_pipeline(request.app.state.CONFIG)

    return {"names": updated_data_sources}

@app.get('/list_datasets',
         summary="get a list of all indexed datasets")
def list_datasets(request: Request) -> Dict[str, List[str]]:
    
    loader = Loader(request.app.state.CONFIG) 

    loader.upload()

    names = loader.get_attribute_from_index('name')

    return {"names": names}

@app.post('/query_datasets',
         summary="Answer a question over all indexed datasets")
def query_datasets(Item: QueryModel, request: Request) -> Dict[str, str]:
    
    answer = query_pipeline(Item.query, request.app.state.CONFIG)

    return {"answer": answer}


@app.post('/query_datasets_test',
         summary="Test version of the endpoint")
def query_datasets(Item: QueryModel, request: Request) -> Dict[str, str]:

    return {"answer": "test answer"}

if __name__ == '__main__':
    uvicorn.run(app)