from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent
from pydantic import SecretStr
import os
from dotenv import load_dotenv
import asyncio
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
print(api_key)

# Initialize the model
llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash-exp', api_key=SecretStr(os.getenv('GEMINI_API_KEY')))
print(llm)

async def main():
    # Create agent with the model
    agent = Agent(
        task="Compare the price of gpt-4o and DeepSeek-V3",
        llm=llm
    )
    print(agent)
    await agent.run()

asyncio.run(main())