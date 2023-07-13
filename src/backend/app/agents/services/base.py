from typing import Any, Dict, Type

from langchain.agents.agent import AgentExecutor
from langchain.agents.agent_types import AgentType
from langchain.agents.agent_toolkits.pandas.base import create_pandas_dataframe_agent
from langchain.schema.language_model import BaseLanguageModel

# TODO: Return number of parsed dataframes


def create_csv_agent(
    llm: BaseLanguageModel,
    datasources_mapper: Dict[str, Type],
    **kwargs: Any,
) -> AgentExecutor:
    
    """Create csv agent by loading to a dataframe and using pandas agent."""

    # Todo: Move try except to dataclass method

    df = []
    for url, dataclass in datasources_mapper.items():
        try:
            df.append(dataclass.read_dataset(url))
        except Exception as e:
            continue

    return create_pandas_dataframe_agent(llm, 
                                         df=df, 
                                         agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION, **kwargs)