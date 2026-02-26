from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langchain_core.messages import HumanMessage,SystemMessage,ToolMessage
from langsmith import traceable
MAX_ITERATIO=10
MODEL="qwen2.5:latest"

@tool
def get_product_price(product:str) -> float:
    """Look up a price of product in catalog."""
    print(f"..... executing get_product_price(product='{product}')")
    prices = {"laptop":70000.56,"headphone":3000.34}
    return prices.get(product,0)

@tool
def get_discount(price:float,discount_tier:str)->float:
    """Apply discount tier to a price and return the final price.
    available tiers : bronze, silver , gold."""
    print(f".... get_discount_tier functiopn called with arguments price = {price} and discount_tier='{discount_tier}'")
    discount_percentage ={"gold":12,"silver":8,"bronze":3}
    discount = discount_percentage.get(discount_tier)
    print(f".... getting discount of {discount} percent on the tier = '{discount_tier}'")
    price = round(price-((price * discount) /100),3)
    return price

@traceable(name=" Agent Loop")
def runAgent(query:str):
    tools=[get_product_price,get_discount]
    tools_dict={t.name:t for t in tools}
    llm = init_chat_model(f"ollama:{MODEL}",temprature=0)
    llm_with_tools=llm.bind_tools(tools)
    print(f"Question is {query}")
    print("="*60)
    messages = [
        SystemMessage(
            content=(
                "You are a helpful shoping assistant. "
                "You have access to product catalog tool "
                "and a discount tool.\n\n"
                "STRICT RULES - you must follow these exactly:\n"
                "1. Never guess or assume any product price. "
                "2. Only call get_discount AFTER you have received "
                " a price from get_product_price. Pass the exact price"
                "returne by get_product_price -  do not pass made up number .\n"
                "3. Never calculate discount yourself using Mathematics. "
                "always use get_discount tool. \n"
                "4. if user doesnt provide the discount tier ask them to provide discount tier. Do not assume one."
            )
        ),
        HumanMessage(
            content=(query
                
            )
        )
    ]

    for iteration in range(1,MAX_ITERATIO+1):
        print(f"\n-- iteration{iteration}")
        ai_message=llm_with_tools.invoke(messages)
        tool_calls = ai_message.tool_calls
        if not tool_calls:
            print(f" final answer {ai_message.content}")
        tool_call = tool_calls[0]
        tool_name=tool_call.get("name")  
        tool_arguments = tool_call.get("args",{})  
        tool_id = tool_call.get("id")
        print(f"tool {tool_name} selected with argument {tool_arguments}")
        tool_to_use= tools_dict.get(tool_name)
        if tool_to_use is None:
            raise ValueError(f"Tool {tool_name} not found")
        observation = tool_to_use.invoke(tool_arguments)
        print(f" Tool result {observation}")

if __name__=="__main__":
    print("hello agent (.build tool)")
    print()
    result = runAgent("What is the price of the laptop after applying the gold discount ?")
