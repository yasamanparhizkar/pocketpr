from google import genai
# from google.generativeai import GenerativeModel
import os

#one way of doing the api call
client = genai.Client(api_key="AIzaSyCUI6IiybH9c04MGPbttx8c2xnm0ajtvHA")
# def ask_question(question):


#     api_key = os.environ.get("AIzaSyCUI6IiybH9c04MGPbttx8c2xnm0ajtvHA")

#     genai.api_key = api_key

#     # model = GenerativeModel('gemini-2.0')
#     # genai.configure(api_key=api_key)
#     model = genai.Client('gemini-pro')

#     try:
#         response = cli.generate_content(question)
#         return response.text.strip()
    
#     except Exception as e:
#         return f"error: {e}"


keep_going = True
count = 1
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


for q in questions:
    answer = input(f"question {count}:" + q)
    answer_tuple = (str(f"question {count}: " + q),str(answer))
    responses_list.append([q, answer])
    count +=1
    

    # questions.append(str(response))
    
# count = 1
# for chunk in answer:
# #     print(chunk.text, end="")
    

# print(response.text)

"""
full prompt used for Gemini:


I would like you to create a LinkedIn post that has a friendly, exciting and fresh tone with the use of emojis when necessary. I also would like the text to be in paragraph form, with space in between the hashtags and the main text. I'd also like some space between the title, date, and the main paragraph. Title and date should be on one line at the top. Here is the information you need to know:

    Q: What is the name of the event? A: GenAI Genesis
    Q: What was the time and place of the event? A: UofT, March 21-23
    Q: What was the purpose of your attendance and your role in the event? A: Attended as a hacker to network, to challenge myself, and to learn lots from peers.
    Q: What were your key takeaways or insights you gained? A: learned about lots of new tools, networked with professionals in the AI and software engineering fields, and produced 
    Q: What was the main theme or purpose of the event? Main theme was AI for Human Empowerment
    "How would you like to frame your call to action?", Ask the readers for their thoughts, or if anyone else attended the event
    "Would you like hashtags at the end of your post for greater reach?" yes

"""
response = client.models.generate_content( #change to generate_content_stream later
    model="gemini-2.0-flash",
    contents="I would like you to create a LinkedIn post that has a friendly, exciting and fresh tone with the use of emojis when necessary. I also would like the text to be in paragraph form, with space in between the hashtags and the main text. I'd also like some space between the title, date, and the main paragraph. Title and date should be on one line at the top. Here is the information you need to know:" + str(responses_list)

)
print(response)
# print (questions)
# print (questions)
# print(responses_list)
