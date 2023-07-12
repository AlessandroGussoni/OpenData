from app.agents.entities import IAbstractAgent
from app.agents.services.base import create_csv_agent

from langchain.llms import OpenAI, OpenAIChat
from app.agents.entities.llms import FakeListLLM

from typing import Dict


class AgentQueryRouter(IAbstractAgent):

    _AGENT_MAPPING = {
        'base_csv': create_csv_agent
    }

    def __init__(self, 
                 query_mapping: Dict[str, str],
                 config: Dict[str, str]) -> None:
        
        self.urls = list(query_mapping.keys())
        agent_type = AgentQueryRouter._AGENT_MAPPING.get(config['agent_loader'], None)
        if not agent_type: raise ValueError("Agent not supported")
        llm = globals()[config['llm']['name']](**config['llm']['kwargs'])

        self.agent = agent_type(llm=llm, datasources_mapper=query_mapping)

    def parse_metainformation(self):
        base_info = "\n Urls dei dataset che potrebbero contenere le informazioni che cerchi: \n"
        urls_string = "\n".join([url for url in self.urls])
        return base_info + urls_string
        

    def __call__(self, query: str) -> str:
        
        answer = self.agent.run(query)

        metainformation = self.parse_metainformation()

        return answer + metainformation


