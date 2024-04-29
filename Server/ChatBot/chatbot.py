from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv('.env')

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.getenv('OPENAI_API_KEY'),
)

model = "gpt-3.5-turbo-0125"
temperature = 0.7
max_tokens = 200


def chatgpt_response(messages):
    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,  
    )
    return completion.choices[0].message.content

def start_conversation():
    print("Welcome to the ChatGPT conversation!")
    print("Type 'new conversation' to start a new conversation.")
    print("Type 'exit' to end the conversation.")
    messages = []
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
        elif user_input.lower() == 'new conversation':
            print("Starting a new conversation...")
            messages = []
            continue
        messages.append({"role": "user", "content": user_input})
        response = chatgpt_response(messages)
        print("ChatGPT:", response)
        messages.append({"role": "system", "content": response})

start_conversation()
