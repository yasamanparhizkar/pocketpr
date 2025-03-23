from google import genai
from google.genai import types
import os

MAX_TEXT_NUM = 100

# instantiate client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
# instantiate decision maker to see if conversation is finished
client_decider = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# instantiate chat with context
chat = client.chats.create(model="gemini-2.0-flash",
                           config=types.GenerateContentConfig(
                               system_instruction="""You are a helpful content creator helping a client write 
                                        a LinkedIn post. Ask relevant and clarifying questions to gain appropriate
                                        information to put in a LinkedIn message. Ask 2-3 questions; 
                                        afterwards, tell the client that you have all the information that you need
                                        and you can proceede with creating the LinkedIn post now.
                                        Ask questions one by one in a natural conversational tone and format. Do NOT ask
                                        multiple questions at once.
                                        One of your questions must be about what tone the post should be in; professional, friendly, etc.
                                        """))

def get_chat_history(chat):
    """Get chat history in string format."""
    script = ""
    for message in chat.get_history():
        script = script + f"role - {message.role}: " + message.parts[0].text + "\n"
    return script

for i in range(MAX_TEXT_NUM):
    response = chat.send_message(input())
    print(response.text)
    # decide whether the conversation is over
    script = get_chat_history(chat)
    decision = client_decider.models.generate_content(
        model="gemini-2.0-flash",
        config=types.GenerateContentConfig(
            system_instruction="""You are a judge. Read a script and decide whether the 'model'
            has gained enough information from the 'user' for a LinkedIn post.
            If enough information is gained, write 'Yes' and otherwise write 'No'.
            Do NOT write any extra words."""),
        contents=script,
    )
    if decision.text.strip() == "Yes":
        break

script = get_chat_history(chat)
print(script)


