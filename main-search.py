from dotenv import load_dotenv

load_dotenv()
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from langchain_tavily import TavilySearch
from langchain_ollama import ChatOllama

#@traceable 
#ollama run functiongemma
def main():
    print("Hello from langchain-course!")
    #llm = ChatOllama(temperature=0, model="gemma3:latest")
    #ollama run qwen2.5
    llm = ChatOllama(temperature=0, model="qwen2.5")
    tools = [TavilySearch(max_results=1)]
    #tools = [search]
    agent=create_agent(model=llm,tools=tools)
    resutl = agent.invoke({"messages":HumanMessage(content="what is the weather in indore india")})
    print (resutl)
@tool
def search(query:str) -> str:
    """
    Tool that search on internet 

    Args:
        query: the query to search for
    Returns:
          the search result     
    """
    print(f"searching for {query}")
    #return "Tokyo Weather is hot"
    return TavilySearch( max_results=1).invoke(query)


def toAdd(number1:int,number2:int) -> str:
    print(f"callin addition of {number1},{number2}")
    return str(number2+number1)



if __name__ == "__main__":
    main()
