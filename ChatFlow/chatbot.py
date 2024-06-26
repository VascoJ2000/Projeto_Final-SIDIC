from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv('.env')

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
model = "gpt-3.5-turbo-0125"


def chatgpt_response(message_list, max_tokens=200, temperature=0.7):
    completion = client.chat.completions.create(
        model=model,
        messages=message_list,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return completion.choices[0].message.content

