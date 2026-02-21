from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama
import google.generativeai as genai
from langsmith import traceable

load_dotenv()
#@traceable
def main():
    print("Hello from langchain-course!")

    information = """
The German Shepherd, also known in Britain as an Alsatian, is a German breed of working dog of medium to large size.
    """
 
    summary_template=""" 
given the information {information} about the german shepard dog i want you to explain:
1. It's body structrue
2. life span.
    """
    summary_prompt_template = PromptTemplate(input_variables=["information"], template=summary_template)
    llm = ChatOllama(temperature=0, model="gemma3:latest")
    chain= summary_prompt_template | llm
    response= chain.invoke(input={"information":information})
    print(response.content)



if __name__ == "__main__":
    main()
