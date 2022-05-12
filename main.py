from flask import Flask, render_template, request
import datetime
import json


app = Flask(__name__)

DB_FILE = "./data/db.json"
db = open(DB_FILE, "rb")
data = json.load(db)
messages = data["messages"]
print(len(messages))

def save_messages_to_file():
    db = open(DB_FILE, "w")
    data = {
        "messages" : messages
    }
    json.dump(data, db)
def add_message(text, sender):
    now = datetime.datetime.now()
    new_message = {
        "text": text,
        "sender": sender,
        "time": now.strftime("%H:%M")
    }
    messages.append(new_message)
    save_messages_to_file()

def check_numbers_of_messages():
    if len(messages)>26:
        del messages[0]
    else:
        return

def print_message(message):
    print(f"[{message['sender']}]: {message['text']} / {message['time']} ")


for message in messages:
    print_message(message)



#формат джейсон
@app.route("/get_messages")
def get_messages():
    return {'messages': messages}

@app.route("/")
def form():
    return render_template("form.html")

@app.route("/send_message")
def send_message():
    check_numbers_of_messages()
    name = request.args["name"]
    text = request.args["text"]
    if len(name) < 3 or len(name) > 100 :
        print("Длина имени пользователя недопустима")
    elif len(text) < 1 or len(text) > 3000:
        print("Длина сообщения недопустима")
    else:
        add_message(text, name)

    return "OK"
@app.route("/clear_data")
def clear_data():
    messages.clear()
    return "messages are clear"

app.run(host="0.0.0.0", port=80)

