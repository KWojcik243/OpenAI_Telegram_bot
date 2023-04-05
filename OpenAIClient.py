from decouple import config
import openai

class OpenAIClient:
  def __init__(self) -> None:
    openai.organization = config("OPENAI_API_ORG")
    openai.api_key = config("OPENAI_API_KEY")
    
  def completion(self, messages) -> str:
    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      user="user1",
      messages=messages
    )
    # [
      #   {"role": "user", "content": "Jak wysoko skacze sowa?"},
      #   {"role": "assistant", "content": "Sowa nie potrafią skakać, ponieważ ich ciało i kończyny nie są przystosowane do skakania. Jednakże, wiele gatunków sów jest w stanie latać z wysokiej wysokości na niską, aby złapać swoją zdobycz."},
      #   {"role": "user", "content": "A kaczka?"}
      # ]

    return completion['choices'][0]['message']['content']