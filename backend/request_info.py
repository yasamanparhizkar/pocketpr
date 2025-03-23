from google import genai
import os
import subprocess
from google.genai import types

import sys
sys.path.append(".")
from backend.post_on_linkedin import main, config, llm, browser, controller

MAX_TEXT_NUM = 100

class chatII():
    """Chat interface."""

    def __init__(self):
        self.main_prompt = ""
        self.questions = [
            "What is the name of the event?", 
            "What was the time and place of the event?", 
            "What was the purpose of your attendance and your role in the event?",
            "What were your key takeaways or insights you gained?",
            # "What was the main theme or purpose of the event?",
            # "How would you like to frame your call to action?",
            # "Would you like hashtags at the end of your post for greater reach?"
        ]
        self.responses_list = []
        self.current_question = -1

        # instantiate the LLM
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    def get_answer(self, input_message: str):
        """Get user input and ask the next question."""
        if self.current_question == -1:
            self.main_prompt = input_message
            next_questions = self.questions[self.current_question + 1]
            self.current_question += 1
        elif self.current_question > -1 and self.current_question < len(self.questions) - 1:
            self.responses_list.append((self.questions[self.current_question], input_message))
            next_questions = self.questions[self.current_question + 1]
            self.current_question += 1
        elif self.current_question == len(self.questions) - 1:
            self.responses_list.append((self.questions[self.current_question], input_message))
            next_questions = "Thanks for your answers! I'm working on the LinkedIn message now."
            self.get_final_post()
            self.current_question += 1
        else:
            next_questions = "Thanks for your answers! I'm working on the LinkedIn message now."
        return next_questions
    
    def get_final_post(self):
        """Make the final post from the responses."""
        prompt = """
            I would like you to create a LinkedIn post with a professional but enthusiastic tone.
            Generate the text in pure text without any html or markdown syntax.
            Do not use emojies. Have between 3 to 5 hashtags at the end.
            Include the information from below question and answer pairs.
        """
        qa = ""
        for (q, a) in self.responses_list:
            qa = qa + f"Question: {q} - " + f"Answer: {a}" + "\n"
        prompt = prompt + qa
        print(prompt)

        # get the final post
        response = self.client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
        with open("backend/message.txt", "w") as file:
            file.write(response.text)

        # call browser-use
        subprocess.call(["python", "backend/post_on_linkedin.py"])

class chatI():
    """Chat interface."""

    def __init__(self):
        # instantiate client
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        # instantiate decision maker to see if conversation is finished
        self.client_decider = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

        self.flag = False

        # instantiate chat with context
        self.chat = self.client.chats.create(model="gemini-2.0-flash",
                                config=types.GenerateContentConfig(
                                    system_instruction="""You are a helpful content creator helping a client write 
                                                a LinkedIn post. Ask relevant and clarifying questions to gain appropriate
                                                information to put in a LinkedIn message. Ask 2-3 questions; 
                                                afterwards, tell the client that you have all the information that you need
                                                and you can proceede with creating the LinkedIn post now.
                                                After gaining enough information about the LinkedIn post, continue conversing in a friendly manner.
                                                Ask questions one by one in a natural conversational tone and format. Do NOT ask
                                                multiple questions at once.
                                                One of your questions must be about what tone the post should be in; professional, friendly, etc.
                                                Be concise. Another question must be about the time and place the event took place.
                                                """))
    
    def get_chat_history(self, chat):
        """Get chat history in string format."""
        script = ""
        for message in chat.get_history():
            script = script + f"role - {message.role}: " + message.parts[0].text + "\n"
        return script

    def get_answer(self, input_message: str):
        """Get user input and ask the next question."""
        response = self.chat.send_message(input_message)
        if not self.flag:
            # decide whether the conversation is over
            script = self.get_chat_history(self.chat)
            decision = self.client_decider.models.generate_content(
                model="gemini-2.0-flash",
                config=types.GenerateContentConfig(
                    system_instruction="""You are a judge. Read a script and decide whether the 'model'
                    has gained enough information from the 'user' for a LinkedIn post.
                    If enough information is gained, write 'Yes' and otherwise write 'No'.
                    Do NOT write any extra words."""),
                contents=script,
            )
            if decision.text.strip() == "Yes":
                self.flag = True
                self.get_final_post(script)
        return response.text
    
    def get_final_post(self, script):
        """Make the final post from the responses."""
        prompt = f"""
            I would like you to create a LinkedIn post with a professional but enthusiastic tone.
            Generate the text in pure text without any html or markdown syntax.
            Do not use emojies. Have between 3 to 5 hashtags at the end.
            Include the information from below interview script.

            {script}
        """

        # get the final post
        response = self.client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
        with open("backend/message.txt", "w") as file:
            file.write(response.text)

        # call browser-use
        subprocess.call(["python", "backend/post_on_linkedin.py"])

if __name__ == "__main__":
    chati = chatI()
    chati.responses_list = [("qdfasd", "fadfas")]
    chati.get_final_post()

