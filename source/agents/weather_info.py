import os
import json
import requests
from ai_provider.openai_connection import openai_connection

class weather_info:

    def __init__(self):
        self = self
        self.weather_api_key = os.environ.get("openweathermap_api_key") 
        self.open_ai_conn = openai_connection()
        

    #------------------------------------------------------
    # GPT Function config - Weather 
    #------------------------------------------------------
    gpt_func_tool_weather = [
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "Get the current weather and temperature in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g. San Francisco, CA",
                        },
                    },
                    "required": ["location"],
                    "additionalProperties": False
                }
            }
        }
    ]


    #------------------------------------------------------
    # Fetch weather data for a city
    #------------------------------------------------------
    def get_weather(self, location) -> str:
        """Fetch weather data for a city."""
        url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={self.weather_api_key}&units=metric'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()        
            return json.dumps(data)
        else:
            return None



    #------------------------------------------------------
    # Chat loop about the weather
    #------------------------------------------------------
    def process_weather_query(self, question):
        """Chat loop about the weather"""   
        messages = [
            {"role": "system", "content": "You are a helpful assistant that provides weather information."},
            {"role": "user", "content": question}
        ]
        
        while True:
            response = self.open_ai_conn.chat_completion_tool_call(messages, self.gpt_func_tool_weather)
            message = response.choices[0].message
            
            if message.tool_calls:
                for tool_call in message.tool_calls:
                    function = tool_call.function
                    if function.name == "get_weather":
                        arguments = json.loads(function.arguments)
                        weather_result = self.get_weather(**arguments)
                        
                        if weather_result is None:
                            error_message = f"Weather service could not find any info about {arguments['location']}"
                            messages.append({"role": "function", "name": "get_weather", "content": error_message})
                        else:
                            messages.append({"role": "function", "name": "get_weather", "content": weather_result})
                        
            else:
                if response.choices[0].finish_reason == "stop":
                    #logging.info(f"Final message: {message.content}")
                    return message.content  #BREAK loop and exit
                
                messages.append({"role": "assistant", "content": message.content})