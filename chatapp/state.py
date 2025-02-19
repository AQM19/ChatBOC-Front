import os
import reflex as rx
import requests
import httpx
from loguru import logger
import os
from dotenv import load_dotenv


class QA(rx.Base):
    """A question and answer pair."""

    question: str
    answer: str

DEFAULT_CHATS = {
    "Intros": [],
}

class State(rx.State):
    """The app state."""

    load_dotenv()

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
            response = httpx.get(os.getenv('BACKEND_URL')+'/user/chats', 
                                 headers=headers, 
                                 cookies=cookies,
                                 timeout=30)
            data = response.json()
            
            if response.status_code != 200:
                return rx.event.window_alert("Server error, please try again.")
            logger.info(data)
            for chat in data:
                self.chats_uuid[chat[1]] = chat[0]
                self.chats[chat[1]] = self.getChat(chat[0],chat[1])
            # If data is not empty, set the last chat as the current chat.
            if data:
                self.current_chat = data[-1][1]
                # Remove DEFAULT_CHATS
                # del self.chats['Intros']
            else:
                self.new_chat_name="New chat"
                self.create_chat()
        except httpx.HTTPStatusError:
            return rx.event.window_alert("Server error, please try again.")
            
            
    
    def getChat(self, chat_id, chat_name):
        '''Get the chat from the server.'''
        if not self.token:
            return rx.event.redirect('/login')        
        cookies = {'session': self.session}
        headers = {'Authorization': f'Bearer {self.token}'}
        try:
            response = httpx.get(os.getenv('BACKEND_URL')+f'/user/chat/{chat_id}/messages', headers=headers,cookies=cookies,timeout=30)
            data = response.json()
            messages = []
            question = ""
            answer = ""
            data.reverse()
            for line in data:
                # manejo de respuesta: lista de listas
                # formato [id, chat_id, user_id, message, is_response, created_at]
                # line[0] -> id
                # line[1] -> chat_id
                # line[2] -> user_id
                # line[3] -> message
                # line[4] -> is_response
                # line[5] -> created_at
                #logger.info(f"Line: {line}")
                if line[4]:
                    answer = line[3]
                else:
                    question = line[3]
                if question and answer:
                    messages.append(QA(question=question, answer=answer))
                    question = ""
                    answer = ""
                # messages.append(QA(question=line[6], answer=line[3]))
            
            return messages
        except httpx.HTTPStatusError:
            return rx.event.window_alert(f"Server error, please try again.{self.session}")

    def login(self,form_data):
        try:
            self.chats = DEFAULT_CHATS
            response = httpx.post(os.getenv('BACKEND_URL')+'/login', 
                                  json={'username': form_data['username'], 'password': form_data['password']},
                                  timeout=30,
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
            
            response = httpx.post(os.getenv('BACKEND_URL')+'/register', 
                                  json=data,
                                  timeout=30
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
            response = httpx.post(os.getenv('BACKEND_URL')+'/user/chat',
                                json=data,
                                headers=headers,
                                cookies=cookies,
                                timeout=30)
            if response.status_code != 200 or not 'chat_id' in response.json():
                return rx.event.window_alert("Server error, please try again.")
            #logger.info(f"Response: {response}")
            data = response.json()
            #logger.info(f"Data: {data}")
            self.chats_uuid[self.new_chat_name] = data['chat_id'][0]
        except httpx.HTTPStatusError:
            return rx.event.window_alert("Server error, please try again.")
        
        
    def delete_chat(self):
        """Delete the current chat."""
        cookies = {'session': self.session}
        headers = {'Authorization': f'Bearer {self.token}'}
        if not self.current_chat in self.chats_uuid:
            return rx.event.window_alert("The current chat has no uuid.")
        logger.info(f"Deleting chat {self.chats_uuid[self.current_chat]}")
        try:
            response = httpx.delete(os.getenv('BACKEND_URL')+f'/user/chat/{self.chats_uuid[self.current_chat]}', 
                                    headers=headers, 
                                    cookies=cookies,
                                    timeout=30)
        except httpx.HTTPStatusError:
            return rx.event.window_alert("Server error, please try again.")
        del self.chats[self.current_chat]
        # logger.info(f"Chats: {self.chats}")
        # logger.info(f"Chats UUID: {self.chats_uuid}")
        # logger.info(len(self.chats))
        if len(self.chats) == 0:
            logger.info("No chats left.")
            self.chats = DEFAULT_CHATS
        self.current_chat = list(self.chats.keys())[-1]

    def set_chat(self, chat_name: str):
        """Set the name of the current chat.

        Args:
            chat_name: The name of the chat.
        """
        self.current_chat = chat_name


    def scroll_to_bottom(self):
        """Scroll to the bottom of the chat."""
        logger.info("Scrolling to bottom")
        
        return rx.scroll_to("chat-end")
    @rx.var
    def chat_titles(self) -> list[str]:
        """Get the list of chat titles.

        Returns:
            The list of chat names.
        """
        return list(self.chats.keys())
    def set_question(self, question: str):
        """Set the current question.

        Args:
            question: The current question.
        """
        #logger.info(f"Question(set_question): {question}")
        self.question = question

    def submit_question(self):
        """Submit a question to the chat.

        Args:
            form_data: A dict with the current question.
        """
        # Get the question from the form
        question = self.question
        #logger.info(f"Question(submit_question): {question}")

        # Check if the question is empty
        if question == "":
            return

        # Add the question to the list of questions. https://www.google.com/url?sa=i&url=https%3A%2F%2Fwpamelia.com%2Floading-animation%2F&psig=AOvVaw2ElavECpD5AHBCmioC6YcR&ust=1717682492076000&source=images&opi=89978449
        #qa = QA(question=question, answer='<img src="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/0.16.1/images/loader-large.gif" alt="procesando respuesta">')
        #qa = QA(question=question, answer='<img src="https://www.google.com/url?sa=i&url=https%3A%2F%2Fwpamelia.com%2Floading-animation%2F&psig=AOvVaw2ElavECpD5AHBCmioC6YcR&ust=1717682492076000&source=images&opi=89978449" alt="procesando respuesta">')
        qa = QA(question=question, answer='<image src="/loader.gif" alt="procesando respuesta" width="30em" height="30em">')
        #qa = QA(question=question, answer='<img src="https://res.cloudinary.com/bytesizedpieces/image/upload/v1656084931/article/a-how-to-guide-on-making-an-animated-loading-image-for-a-website/animated_loader_gif_n6b5x0.gif" alt="procesando respuesta" width="30" height="20">')
        self.chats[self.current_chat].append(qa)
        return rx.scroll_to("chat-end")
    
    
    def process_question_llama(self, form_data: dict[str, str]):
        # Get the question from the form
        question = form_data["question"]

        # Check if the question is empty
        if question == "":
            return
        
        self.processing = True
        self.llama_process_question(question)
        return self.scroll_to_bottom()      
        # return rx.client_side(
        #     f"document.getElementById('scrollable-chat').scrollTo(0, document.getElementById('scrollable-chat').scrollHeight);"
        # )
    
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

        # Clear the input and start the processing.
        self.processing = True
        yield

        cookies = {'session': self.session}
        headers = {'Authorization': f'Bearer {self.token}'}
        response = httpx.get(os.getenv('BACKEND_URL')+f'/?question={question}&chat_id={self.chats_uuid[self.current_chat]}',
                              headers=headers,
                              cookies=cookies, 
                              timeout=None)
        answer_text=None
        if not response or response.status_code != 200:
            self.chats[self.current_chat][-1].answer += "Sorry, I couldn't get a response from the server."
        else:
            #logger.info(f"Response: {response}")
            answer_text = response.json()['message']
            if answer_text is not None:

                self.chats[self.current_chat][-1].answer = answer_text
            else:
                answer_text = ""
                self.chats[self.current_chat][-1].answer += answer_text
            self.chats = self.chats
            yield
        
        self.scroll_to_bottom()

        # Toggle the processing flag.
        self.processing = False
        yield

    def llama_process_question(self, question: str):

        """Get the response from the API.

        Args:
            form_data: A dict with the current question.
        """
        # Clear the input and start the processing.
        self.processing = True
        

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
        response = httpx.get(os.getenv('BACKEND_URL')+f'/?question={question}&chat_id={self.chats_uuid[self.current_chat]}',
                              headers=headers,
                              cookies=cookies, 
                              timeout=None)
        answer_text=None
        if not response or response.status_code != 200:
            self.chats[self.current_chat][-1].answer += "Sorry, I couldn't get a response from the server."
        else:
            #logger.info(f"Response: {response.json()}")
            answer_text = response.json()['message']
            if answer_text is not None:
                self.chats[self.current_chat][-1].answer = answer_text
            else:
                answer_text = ""
                self.chats[self.current_chat][-1].answer += answer_text
            self.chats = self.chats
            

        # Toggle the processing flag.
        self.processing = False
        return