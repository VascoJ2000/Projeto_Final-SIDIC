from flask import Flask, request, jsonify
import openai

app = Flask(__name__)
openai.api_key = 'sk-proj-OJo3J21KQm6tE5PNGPQST3BlbkFJJWfP5vW83EZvxkhZGe2S'
@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data['question']
    response = ask_gpt3(question)
    return jsonify({'response': response})

def ask_gpt3(question):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=question,
        temperature=0.7,
        max_tokens=100
    )
    return response.choices[0].text.strip()

if __name__ == '__main__':
    app.run(debug=True)