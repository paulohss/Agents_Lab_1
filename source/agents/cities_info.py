import json
from ai_provider.openai_connection import openai_connection

class cities_info:
    
    def __init__(self):
        self = self
        self.open_ai_conn = openai_connection()
    
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
    # Chat loop about fetching language info about cities
    #------------------------------------------------------
    def process_language_info(self, question):
        """Chat loop about fetching language info about cities"""   
        messages = [
            {"role": "system", "content": "You are a helpful assistant that provides spoken languages info and cities."},
            {"role": "user", "content": question}
        ]
        
        response = self.open_ai_conn.chat_completion_func_call(messages, self.gpt_func_lang_info, {"name":"setLanguages"})
        message = response.choices[0].message
        
        if message.function_call.name != "setLanguages":
            raise ValueError("[setLanguages] not identified by OpenAI api. ")
            
        return json.loads(message.function_call.arguments)