import os
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.llms import OpenAI


llm = OpenAI(temperature=0)
tools = load_tools(["serpapi"], llm=llm) # "llm-math"

agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION)
response = agent.invoke("Who is Leo DiCaprio's girlfriend name AND What is her current age raised to the 0.43 power?")
print(response)
