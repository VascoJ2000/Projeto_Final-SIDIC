import openai

openai.api_key = 'sk-proj-OJo3J21KQm6tE5PNGPQST3BlbkFJJWfP5vW83EZvxkhZGe2S'

def ask_gpt3(question):
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",  
        prompt=question,
        temperature=0.7,  # Controls the randomness of the response
        max_tokens=100  # Controls the length of the response
    )
    return response.choices[0].text.strip()

question = "What is the capital of France?"
answer = ask_gpt3(question)
print(answer)