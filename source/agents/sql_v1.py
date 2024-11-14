import os
from langchain.agents import *
from urllib.parse import quote_plus
from langchain_community.chat_models import ChatOpenAI
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from sqlalchemy import create_engine
from langchain_core.globals import set_verbose, set_debug


class sql_v1:
    
        def __init__(self, verbose = False):   
            set_debug(verbose)
            set_verbose(verbose)         
            self.create_db()
            self.create_llm_agent()
        
        
        def create_db(self):
            self.server = "User-PC"
            self.database = "Invoice"
            self.conn_str = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.server};DATABASE={self.database};Trusted_Connection=yes;"
            self.engine = create_engine(f"mssql+pyodbc:///?odbc_connect={quote_plus(self.conn_str)}")
            self.db = SQLDatabase(self.engine)
            
            
        def create_llm_agent(self):
            self.llm = ChatOpenAI(model="gpt-4")
            self.tool_kit = SQLDatabaseToolkit(db=self.db, llm=self.llm)
            self.agent_executor = create_sql_agent(
                        llm=self.llm,
                        toolkit=self.tool_kit,
                        verbose=True
                    )


        def talk(self, question: str) -> str:
            response = self.agent_executor.invoke(question)
            return response['output']