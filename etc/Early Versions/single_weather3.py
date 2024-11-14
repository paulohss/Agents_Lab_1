import json
import os
import requests
from openai import OpenAI
from datetime import datetime, timedelta
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set the API key and model name
MODEL = "gpt-4"
client = OpenAI(api_key=os.environ.get("openAiKey"))
weather_api_key = os.environ.get("openweathermap_api_key") 

#------------------------------------------------------
# Fetch weather data for a city
#------------------------------------------------------
def get_weather(location) -> str:
    """Fetch weather data for a city."""
    url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={weather_api_key}&units=metric'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()        
        return json.dumps(data)
    else:
        return None

#------------------------------------------------------
# GPT Function config - Weather 
#------------------------------------------------------
gpt_func_weather = [
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
# GPT Function config - Language
#------------------------------------------------------
gpt_func_lang_info = [
    {
        "name": "setLanguages",
        "description": "Sets the main language spoken in a number of cities",
        "parameters": {
            "type": "object",
            "properties": {
                "cities": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "city": {
                                "type": "string"
                            },
                            "language": {
                                "type": "string"
                            }
                        },
                        "required": [
                            "city",
                            "language"
                        ]
                    }
                }
            },
            "required": [
                "cities"
            ]
        }
    }    
]


#------------------------------------------------------
# Call OpenAI chat completion API   
#------------------------------------------------------
def callOpenAi(messageList, gpt_func):
    """Call OpenAI chat completion API"""    
    response = client.chat.completions.create(
        model=MODEL,
        messages=messageList,
        tools=gpt_func
    )
    return response


def callOpenAi_func_call(messageList, gpt_functions, gpt_function_call):
    """Call OpenAI chat completion API"""    
    response = client.chat.completions.create(
        model=MODEL,
        messages=messageList,
        functions= gpt_functions,
        function_call=gpt_function_call
    )
    return response



#------------------------------------------------------
# Chat loop about the weather
#------------------------------------------------------
def process_weather_query(question):
    """Chat loop about the weather"""   
    messages = [
        {"role": "system", "content": "You are a helpful assistant that provides weather information."},
        {"role": "user", "content": question}
    ]
    
    while True:
        response = callOpenAi(messages, gpt_func_weather)
        message = response.choices[0].message
        
        if message.tool_calls:
            for tool_call in message.tool_calls:
                function = tool_call.function
                if function.name == "get_weather":
                    arguments = json.loads(function.arguments)
                    weather_result = get_weather(**arguments)
                    
                    if weather_result is None:
                        error_message = f"Weather service could not find any info about {arguments['location']}"
                        messages.append({"role": "function", "name": "get_weather", "content": error_message})
                    else:
                        messages.append({"role": "function", "name": "get_weather", "content": weather_result})
                    
        else:
            if response.choices[0].finish_reason == "stop":
                logging.info(f"Final message: {message.content}")
                return message.content  #BREAK loop and exit
            
            messages.append({"role": "assistant", "content": message.content})



#------------------------------------------------------
# Chat loop about fetching language info about cities
#------------------------------------------------------
def process_language_info(question):
    """Chat loop about fetching language info about cities"""   
    messages = [
        {"role": "system", "content": "You are a helpful assistant that provides spoken languages info and cities."},
        {"role": "user", "content": question}
    ]
    
    response = callOpenAi_func_call(messages, gpt_func_lang_info, {"name":"setLanguages"})
    message = response.choices[0].message
    
    if message.function_call.name != "setLanguages":
        raise ValueError("[setLanguages] not identified by OpenAI api. ")
        
    return json.loads(message.function_call.arguments)


#-----------------------------------------------------------------
# Program entry point
#-----------------------------------------------------------------
def main():
    while True:          
        choice = input("\n[1] for General question.  \n[2] for Weather info.  \n[3] for Language info as json. \nType on of the numbers above to continue:")
        
        if choice.strip().lstrip() == "1":
            print("---")
        
        elif choice.strip().lstrip() == "2":     
            question = input("Ask about the WEATHER (or type 'exit' to quit): ")
            if question.lower() == 'exit':
                break  #BREAK loop and exit
        
            result = process_weather_query(question)
            print(result)
            
        elif choice.strip().lstrip() == "3":         
            question = input("Ask about CITIES and LANGUAGES (or type 'exit' to quit): ")
            if question.lower() == 'exit':
                break  #BREAK loop and exit
            
            result = process_language_info(question)
            print(result)
        
        else:
            break

if __name__ == "__main__":
    main()