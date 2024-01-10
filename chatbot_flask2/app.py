from flask import Flask, render_template, request
import openai
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

openai.api_key = os.environ.get('YOUR_API_KEY')
openai.api_base = "https://api.openai.iniad.org/api/v1"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    amount_tokens = 0
    chat = []

    setting = request.form.get('setting')
    if setting == "y" or setting == "Y":
        content = request.form.get('content')
        chat.append({"role": "system", "content": content})

    user_input = request.form.get('user_input')
    if user_input.lower() == "q" or user_input.lower() == "quit":
        return f"トークン数は{amount_tokens}でした。"

    chat.append({"role": "user", "content": user_input})
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=chat)
    msg = response["choices"][0]["message"]["content"].lstrip()
    amount_tokens += response["usage"]["total_tokens"]
    chat.append({"role": "assistant", "content": msg})

    return render_template('chat.html', user_input=user_input, assistant_response=msg)

if __name__ == "__main__":
    app.run(debug=True)
