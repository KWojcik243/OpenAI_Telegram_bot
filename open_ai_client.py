from decouple import config
import openai

from db_setup import DbSetup

class OpenAIClient:
	def __init__(self) -> None:
		openai.organization = config("OPENAI_API_ORG")
		openai.api_key = config("OPENAI_API_KEY")
		self.db = DbSetup()
		
	def completion(self, messages, user_id) -> str:
		"""
		Generates a response to a user's message using the OpenAI API, and saves the generated message to the connected PostgreSQL database.

		Args:
			messages (list of str): A list of strings representing the conversation history leading up to the user's message.
			user_id (int): The unique identifier of the user who sent the message.
			
		Returns:
			bot_message (str): A string representing the response generated by the OpenAI API.
		"""
		completion = openai.ChatCompletion.create(
			model="gpt-3.5-turbo",
			messages=messages
		)
		
		bot_message = completion['choices'][0]['message']['content']
		self.db.insert_mess(role="assistant", message=bot_message, user_id=user_id)
		return bot_message