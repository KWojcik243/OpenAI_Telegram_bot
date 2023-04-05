from decouple import config
import openai
openai.organization = config("OPENAI_API_ORG")
openai.api_key = config("OPENAI_API_KEY")
completion = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "user", "content": "Hello!"}
  ]
)

print(completion.choices[0].message)