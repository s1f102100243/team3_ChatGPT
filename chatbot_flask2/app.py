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

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        amount_tokens = 0
        chat = []
        
        # Group discussion inputs.
        group_discussion_inputs = {
            "member1": request.form.get('member1_input', ''),
            "member2": request.form.get('member2_input', ''),
            "member3": request.form.get('member3_input', ''),
            "member4": request.form.get('member4_input', ''),
            "member5": request.form.get('member5_input', ''),
            "member6": request.form.get('member6_input', ''),
            "member7": request.form.get('member7_input', ''),
            "member8": request.form.get('member8_input', ''),
            "member9": request.form.get('member9_input', ''),
            "member10": request.form.get('member10_input', ''),
        }
        
        discussion_content = []
        for member, content in group_discussion_inputs.items():
            if content:
                formatted_content = f"{member} ({content})"
                discussion_content.append(formatted_content)
                
        # Process group discussion first, if any.
        group_discussion_text = '\n'.join(discussion_content)
        if group_discussion_text:
            chat.append({"role": "system", "content": group_discussion_text})
        
        # Process other chat inputs
        setting = request.form.get('setting', '')
        if setting.lower() in ['y', 'yes']:
            content = request.form.get('content', '')
            chat.append({"role": "system", "content": content})
        
        user_input = request.form.get('user_input', '')
        if user_input.lower() in ['q', 'quit']:
            return f"トークンの合計数: {amount_tokens}"

        # User input is added to chat
        chat.append({"role": "user", "content": user_input})
        
        # Personality statements (assuming these fields exist in your form)
        # Collect these only if you need them for the conversation
        personalities = {key: request.form.get(key, '') for key in ['personality_1', 'personality_2', 'personality_3', 'personality_4', 'personality_5', 'personality_6', 'personality_7', 'personality_8', 'personality_9', 'personality_10']}
        personality_statements = [f"{key[-1]}: {value}" for key, value in personalities.items() if value]
        
        if personality_statements:
            chat.append({"role": "assistant", "content": "\n".join(personality_statements)})
        
        # Call the OpenAI API for a chat response
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=chat)
        assistant_msg = response["choices"][0]["message"]["content"].strip()
        amount_tokens += response["usage"]["total_tokens"]
        chat.append({"role": "assistant", "content": assistant_msg})
        
        return render_template('chat.html', user_input=user_input, assistant_response=assistant_msg, discussion_response=group_discussion_text)
    
    else:
        # Render the initial form
        return render_template('chat.html')

# ... Additional routes and application setup if needed.

if __name__ == '__main__':
    app.run(debug=True)