from google import genai
import os
import asyncio
import subprocess

import sys
sys.path.append(".")
from backend.post_on_linkedin import main, config, llm, browser, controller


class chatI():
    """Chat interface."""

    def __init__(self):
        self.main_prompt = ""
        self.questions = [
            "What is the name of the event?", 
            "What was the time and place of the event?", 
            "What was the purpose of your attendance and your role in the event?",
            "What were your key takeaways or insights you gained?",
            "What was the main theme or purpose of the event?",
            "How would you like to frame your call to action?",
            "Would you like hashtags at the end of your post for greater reach?"
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
            I would like you to create a LinkedIn post that has a friendly,
            exciting and fresh tone with the use of emojis when necessary.
            I also would like the text to be in paragraph form, with space in
            between the hashtags and the main text. I'd also like some space between
            the title, date, and the main paragraph.
            Title and date should be on one line at the top.
            Here is the information you need to know:
        """
        qa = ""
        for (q, a) in self.responses_list:
            qa = qa + f"Question: {q} - " + f"Answer: {a}" + "\n"
        prompt = prompt + qa

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

