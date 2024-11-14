import os
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.llms import OpenAI
from langchain_core.globals import set_verbose, set_debug

class google_search:
    
    def __init__(self, verbose=False): 
        set_debug(verbose)
        set_verbose(verbose)       
        self.llm = OpenAI(temperature=0)
        self.tools = load_tools(["serpapi"], llm=self.llm) # uses serpapi to do the google search

    
    #------------------------------------------------------
    # Run the LLM Agent for a google search
    #------------------------------------------------------
    def search_question(self, question: str) -> str:
        agent = initialize_agent(self.tools, self.llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION)
        response = agent.invoke(question)
        return response['output']
