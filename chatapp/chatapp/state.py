import os
import reflex as rx
import requests
import httpx
from chatapp.env import JWT_SECRET_KEY, SECRET_KEY
from loguru import logger


class QA(rx.Base):
    """A question and answer pair."""

    question: str
    answer: str

DEFAULT_CHATS = {
    "Intros": [],
}

class State(rx.State):
    """The app state."""

    # A dict from the chat name to the list of questions and answers.
    chats: dict[str, list[QA]] = DEFAULT_CHATS
    chats_uuid: dict[str, str] = {}
    # The current chat name.
    current_chat = "Intros"

    # The current question.
    question: str

    # Whether we are processing the question.
    processing: bool = False

    # The name of the new chat.
    new_chat_name: str = ""
    username: str = ""
    password: str = ""
    form_data: dict[str, str] = {}
    token: str = ""
    user_id: str = ""
    session: str = ""
    

    def getChats(self):
        '''Get the chats from the server.'''
        if not self.token:
            return rx.event.redirect('/login')
        cookies = {'session': self.session}
        headers = {'Authorization': f'Bearer {self.token}'}
        try:
            response = httpx.get('http://localhost:5000/user/chats', headers=headers, cookies=cookies)
            data = response.json()
            
            if response.status_code != 200:
                return rx.event.window_alert("Server error, please try again.")
            
            for chat in data:
                self.chats_uuid[chat[1]] = chat[0]
                self.chats[chat[1]] = self.getChat(chat[0],chat[1])
        except httpx.HTTPStatusError:
            return rx.event.window_alert("Server error, please try again.")
            #self.current_chat = chat[0]
            
    
    def getChat(self, chat_id, chat_name):
        '''Get the chat from the server.'''
        if not self.token:
            return rx.event.redirect('/login')        
        cookies = {'session': self.session}
        headers = {'Authorization': f'Bearer {self.token}'}
        try:
            response = httpx.get(f'http://localhost:5000/user/chat/{chat_id}/messages', headers=headers,cookies=cookies)
            data = response.json()
            messages = []
            for line in data:
                messages.append(QA(question=line[6], answer=line[3]))
            return messages
        except httpx.HTTPStatusError:
            return rx.event.window_alert(f"Server error, please try again.{self.session}")

    def login(self,form_data):
        try:
            
            response = httpx.post('http://localhost:5000/login', 
                                  json={'username': form_data['username'], 'password': form_data['password']},
                                  )
            response.raise_for_status()
            data = response.json()
            self.session=response.cookies['session']
            
            if 'access_token' in data:
                self.token = data['access_token']
                self.username = form_data['username']
                
                if 'user_id' in data:
                    self.user_id = data['user_id']
                    self.chats = None
                return rx.event.redirect('/')  # Redirect to the main page
            else:
                return rx.event.window_alert("Invalid login credentials.")
        except httpx.HTTPStatusError:
            return rx.event.window_alert("Server error, please try again.")
    def register(self,form_data):
        try:
            data = {
                'username': form_data['username'],
                'password': form_data['password'],
                'email': form_data['email']
            }
            
            response = httpx.post('http://localhost:5000/register', 
                                  json=data,
                                  )
            response.raise_for_status()
            data = response.json()
            return rx.event.redirect('/')
            
        except httpx.HTTPStatusError:
            return rx.event.window_alert("Server error, please try again.")
        return True
    def create_chat(self):
        """Create a new chat."""
        # Add the new chat to the list of chats.
        self.current_chat = self.new_chat_name
        self.chats[self.new_chat_name] = []
        cookies = {'session': self.session}
        headers = {'Authorization': f'Bearer {self.token}','Content-Type': 'application/json'}
        data = {
            'chat_name': self.new_chat_name
        }
        try:
            response = httpx.post('http://localhost:5000/user/chat',
                                json=data,
                                headers=headers,
                                cookies=cookies)
            if response.status_code != 200 or not 'chat_id' in response.json():
                return rx.event.window_alert("Server error, please try again.")
            logger.info(f"Response: {response}")
            data = response.json()
            logger.info(f"Data: {data}")
            self.chats_uuid[self.new_chat_name] = data['chat_id'][0]
        except httpx.HTTPStatusError:
            return rx.event.window_alert("Server error, please try again.")
        
        
    def delete_chat(self):
        """Delete the current chat."""
        cookies = {'session': self.session}
        headers = {'Authorization': f'Bearer {self.token}'}
        try:
            response = httpx.delete(f'http://localhost:5000/user/chat/{self.chats_uuid[self.current_chat]}', headers=headers, cookies=cookies)
        except httpx.HTTPStatusError:
            return rx.event.window_alert("Server error, please try again.")
        del self.chats[self.current_chat]
        if len(self.chats) == 0:
            self.chats = DEFAULT_CHATS
        self.current_chat = list(self.chats.keys())[0]

    def set_chat(self, chat_name: str):
        """Set the name of the current chat.

        Args:
            chat_name: The name of the chat.
        """
        
        self.current_chat = chat_name

    @rx.var
    def chat_titles(self) -> list[str]:
        """Get the list of chat titles.

        Returns:
            The list of chat names.
        """
        return list(self.chats.keys())

    async def process_question(self, form_data: dict[str, str]):
        # Get the question from the form
        question = form_data["question"]

        # Check if the question is empty
        if question == "":
            return

        model = self.openai_process_question

        async for value in model(question):
            yield value

    async def openai_process_question(self, question: str):
        """Get the response from the API.

        Args:
            form_data: A dict with the current question.
        """

        # Add the question to the list of questions.
        qa = QA(question=question, answer="")
        self.chats[self.current_chat].append(qa)

        # Clear the input and start the processing.
        self.processing = True
        yield

        # Build the messages.
        messages = [
            {
                "role": "system",
                "content": "You are a friendly chatbot named chatBOC. Respond in markdown.",
            }
        ]
        for qa in self.chats[self.current_chat]:
            messages.append({"role": "user", "content": qa.question})
            messages.append({"role": "assistant", "content": qa.answer})

        # Remove the last mock answer.
        messages = messages[:-1]

        # The following commented-out section is for OpenAI API call simulation.
        # Uncomment and use it if you have OpenAI setup.
        #
        # session = OpenAI().chat.completions.create(
        #     model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
        #     messages=messages,
        #     stream=True,
        # )
        #
        # Stream the results, yielding after every word.
        # for item in session:
        #     if hasattr(item.choices[0].delta, "content"):
        #response = requests.get("http://localhost:5000/")
        cookies = {'session': self.session}
        headers = {'Authorization': f'Bearer {self.token}'}
        response = httpx.get(f'http://localhost:5000/?question={question}&chat_id={self.chats_uuid[self.current_chat]}', headers=headers, cookies=cookies, timeout=None)
        
        if not response or response.status_code != 200:
            self.chats[self.current_chat][-1].answer += "Sorry, I couldn't get a response from the server."
        else:
            
            answer_text = response.json()
            if answer_text is not None:
                self.chats[self.current_chat][-1].answer += answer_text
            else:
                answer_text = ""
                self.chats[self.current_chat][-1].answer += answer_text
            self.chats = self.chats
            yield
        

        # Toggle the processing flag.
        self.processing = False
        yield 
