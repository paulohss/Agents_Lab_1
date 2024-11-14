import json
import os
import requests
from openai import OpenAI
from datetime import datetime, timedelta


## Set the API key and model name
MODEL="gpt-4o"
client = OpenAI(api_key=os.environ.get("openAiKey"))
weather_api_key = "05c7f02de64c1924f1b11656ecd8d498"

def get_weather(location) -> str:
    """Fetch weather data for a city."""
    url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={weather_api_key}&units=metric'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()        
        return json.dumps(data)
    else:
        return None


tools = [
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



def callOpenAi(messageList):
    """Call OpenAI chat completion API"""    
    response = client.chat.completions.create(
        model=MODEL,
        messages=messageList,
        tools=tools
        )
    return response




question = input("Ask about the weather: ")
messages = []
messages.append({"role": "system", "content": "you will give short answers"})
messages.append({"role": "user", "content": question})
response = callOpenAi(messages)


#print(json.dumps(response.choices[0].message.model_dump(), indent=2))
function = response.choices[0].message.tool_calls[0].function
if function != None:
    arguments = json.loads(function.arguments)
    function_name = function.name
    function_call = eval(function_name) # delegate/reflection

    weather_result = function_call(**arguments) # "**" unpack arguments & call the function - it's equivalent to get_wheather(location="City Name")
    
    if(weather_result == None):
        print(f"Weather service could not find any info about {arguments}")
    else:
        messages.append({"role":"function", "name": function_name, "content": weather_result })
        response = callOpenAi(messages)    
        print(response.choices[0].message.content)

