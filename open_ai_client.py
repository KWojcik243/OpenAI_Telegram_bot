from decouple import config
import openai

from db_setup import DbSetup

class OpenAIClient:
  def __init__(self) -> None:
    openai.organization = config("OPENAI_API_ORG")
    openai.api_key = config("OPENAI_API_KEY")
    self.db = DbSetup()
    
  def completion(self, messages, user_id) -> str:
    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=messages
    )
    
    bot_message = completion['choices'][0]['message']['content']
    self.db.insert_mess(role="assistant", message=bot_message, user_id=user_id)
    return bot_message