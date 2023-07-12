from typing import Any, Dict, Type

from langchain.agents.agent import AgentExecutor
from langchain.agents.agent_toolkits.pandas.base import create_pandas_dataframe_agent
from langchain.schema.language_model import BaseLanguageModel


def create_csv_agent(
    llm: BaseLanguageModel,
    datasources_mapper: Dict[str, Type],
    **kwargs: Any,
) -> AgentExecutor:
    
    """Create csv agent by loading to a dataframe and using pandas agent."""

    df = [dataclass.read_dataset(url) for url, dataclass in datasources_mapper.items()]

    return create_pandas_dataframe_agent(llm, df, **kwargs)