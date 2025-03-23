from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent, Controller
from browser_use.browser.browser import Browser, BrowserConfig
from pydantic import SecretStr
import os
from dotenv import load_dotenv
import asyncio
from dataclasses import dataclass
load_dotenv()

@dataclass
class Config:
    gemini_api_key: str
    base_url: str
    post: str
    chrome_path: str = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    headless: bool = False
    model: str = "gemini-2.0-flash-exp"
    

# setup configs
config = Config(
        gemini_api_key=os.getenv("GEMINI_API_KEY"),
        base_url="https://www.linkedin.com/feed/",
        post="Hello World!"
    )


# initialize the model
llm = ChatGoogleGenerativeAI(model=config.model, api_key=SecretStr(config.gemini_api_key))

browser = Browser(
        config=BrowserConfig(
            headless=config.headless,
            chrome_instance_path=config.chrome_path
        )
    )

controller = Controller()

async def main():
    # create agent with the model
    print(config)
    agent = Agent(
        task=f"""Navigate to LinkedIn and post a message.

        Here are the steps you need to follow:
        1. Navigate to {config.base_url}
        2. Click on the text bar saying "Share a post".
        3. In the pop up window, type the following message: "{config.post}"
        """,
        llm=llm,
        browser=browser,
        controller=controller,
    )
    history = await agent.run()
    print(f"RESULT: {history}")

asyncio.run(main())