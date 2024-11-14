
from openai import OpenAI
import logging
import os


class openai_connection:

    def __init__(self):
        self = self
        
    # Set up logging
    logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

    # Set the API key and model name
    MODEL = "gpt-4"
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    #------------------------------------------------------
    # Call OpenAI chat completion API   
    #------------------------------------------------------
    def chat_completion_tool_call(self, messageList, gpt_tool):
        """Call OpenAI chat completion API"""    
        response = self.client.chat.completions.create(
            model=self.MODEL,
            messages=messageList,
            tools=gpt_tool
        )
        return response

    #------------------------------------------------------
    # Call OpenAI chat completion API   
    #------------------------------------------------------
    def chat_completion_func_call(self, messageList, gpt_functions, gpt_function_call):
        """Call OpenAI chat completion API"""    
        response = self.client.chat.completions.create(
            model=self.MODEL,
            messages=messageList,
            functions= gpt_functions,
            function_call=gpt_function_call
        )
        return response