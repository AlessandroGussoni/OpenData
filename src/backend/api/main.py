from fastapi import FastAPI, APIRouter, Request
from contextlib import asynccontextmanager

from fastapi.openapi.docs import get_swagger_ui_html

from backend.app.pipelines import update_pipeline, extract_classes_from_file

import uvicorn
from typing import List, Dict
import json


@asynccontextmanager
async def lifespan(app: FastAPI):
    ''' Run at startup
        Initialise the Client and add it to app.state
    '''
    with open(r"src\backend\config.json", 'rb') as file:
        app.state.CONFIG = json.load(file)
    yield


app = FastAPI(lifespan=lifespan)


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
def update_data_sources(request: Request) -> Dict[str, bool]:

    flags = update_pipeline(request.app.state.CONFIG)

    return 





if __name__ == '__main__':
    uvicorn.run(app)