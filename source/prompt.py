from agents.weather_info import weather_info
from agents.google_search import google_search
from agents.sql_v1 import sql_v1
import logging
import warnings
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
colorama_init()
warnings.filterwarnings("ignore")

def print_color(text: str):
    print(f"{Fore.GREEN}{text}{Style.RESET_ALL}")

#-----------------------------------------------------------------
# Program entry point
#-----------------------------------------------------------------
def main():
    while True:          

        print_color("\n[1] for General question.  \n[2] for Weather info.  \n[3] AI Google search. \n[4] Talk to the invoice DB.  ") 
        choice = input("Type on of the numbers above to continue:")

        if choice.strip().lstrip() == "1":
            print("---")
        
        elif choice.strip().lstrip() == "2":     
            question = input("Ask about the WEATHER (or type 'exit' to quit): ")
            if question.lower() == 'exit':
                break  #BREAK loop and exit
            weather = weather_info()
            result = weather.process_weather_query(question)
            print_color(result)
        
        elif choice.strip().lstrip() == "3":     
            question = input("Ask your question (or type 'exit' to quit): ")
            if question.lower() == 'exit':
                break  #BREAK loop and exit
            google = google_search()
            result = google.search_question(question)
            print_color(result)

            
        elif choice.strip().lstrip() == "4":     
            question = input("Chat with the Invoice DB (or type 'exit' to quit): ")
            if question.lower() == 'exit':
                break  #BREAK loop and exit
            invoice = sql_v1()
            result = invoice.talk(question)
            print_color(result)

            
        else:
            break
        
        '''
        elif choice.strip().lstrip() == "3":         
            question = input("Ask about CITIES and LANGUAGES (or type 'exit' to quit): ")
            if question.lower() == 'exit':
                break  #BREAK loop and exit            
            cities = cities_info()
            result = cities.process_language_info(question)
            print(result)
        '''    


if __name__ == "__main__":
    main()