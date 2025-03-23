from google import genai
import os

# get API key
gemini_api_key = os.getenv("GEMINI_API_KEY")

# create client
client = genai.Client(api_key=gemini_api_key)

# create the prompt
questions = [
    "What is the name of the event?", 
    "What was the time and place of the event?", 
    "What was the purpose of your attendance and your role in the event?",
    "What were your key takeaways or insights you gained?",
    "What was the main theme or purpose of the event?",
    "How would you like to frame your call to action?",
    "Would you like hashtags at the end of your post for greater reach?"
]
prompt = f"""You are a content creator gathering information for a LinkedIn post.

You want to gain the answer to the following questions:
{"    ".join(questions)}

And any other relevant information.
"""

response = client.models.generate_content(
    model="gemini-2.0-flash", contents=prompt
)

print(response.text)
