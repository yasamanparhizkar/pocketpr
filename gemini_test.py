from google import genai
from google.generativeai import GenerativeModel
import os

#one way of doing the api call
client = genai.Client(api_key="AIzaSyCUI6IiybH9c04MGPbttx8c2xnm0ajtvHA")
def ask_question(question):


    api_key = os.environ.get("AIzaSyCUI6IiybH9c04MGPbttx8c2xnm0ajtvHA")

    genai.api_key = api_key

    model = GenerativeModel('gemini-2.0')

    try:
        response = model.generate_content(question, stream = False)
        return response.text.strip()
    
    except Exception as e:
        return f"error: {e}"


keep_going = True
count = 0
questions = [
    "What is the name of the event?", 
    "What was the time and place of the event?", 
    "What was the purpose of your attendance and your role in the event?",
    "What were your key takeaways or insights you gained?",
    "What was the main theme or purpose of the event?",
    "How would you like to frame your call to action?",
    "Would you like hashtags at the end of your post for greater reach?"
]
responses_list = []
#ask gemini to ask the question
response = client.models.generate_content( #change to generate_content_stream later
    model="gemini-2.0-flash",
    contents="I want you to write me a linkedin post about an event I went to. Ask me questions regarding the event."
)

for q in questions:
    answer = input(ask_question(q))
    # answer_tuple = (str(f"question {i}: " + q),str(answer))

    responses_list.append([q, answer])
    # count +=1
    


    # questions.append(str(response))
    
# count = 1
# for chunk in answer:
# #     print(chunk.text, end="")
    

# print(response.text)

# print (questions)
print (questions)
print(responses_list)
