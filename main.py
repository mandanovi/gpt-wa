from flask import Flask, request, session
import openai
import os
from dotenv import load_dotenv
from twilio.twiml.messaging_response import MessagingResponse


app = Flask(__name__)
load_dotenv()
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")


@app.route("/", methods=["GET", "POST"])
def bot():
    user_msg = request.values.get('Body', '').lower()
    print(user_msg)
    response = MessagingResponse()
    session['user_question'] = user_msg
    openai.api_key = os.environ.get("API_TOKEN")
    ai_answer = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[
        {"role": "system", "content": session['user_question']},
        {"role": "user", "content": session['user_question']},
        {"role": "assistant", "content": session.get('assistant_answer', '')},
        {"role": "user", "content": user_msg}])
    result = ai_answer["choices"][0]["message"]["content"]
    print(result)
    response.message(result)
    session['assistant_answer'] = result
    return str(response)


if __name__ == "__main__":
    app.run(port=8000, debug=True)
