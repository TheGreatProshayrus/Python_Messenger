from flask import Flask, render_template, request
import datetime
import json


app = Flask(__name__) #создание сервера Фласк

DB_FILE = "./data/db.json"
db = open(DB_FILE, "rb")
data = json.load(db)
messages = data["messages"]
print(len(messages))

def save_messages_to_file():    # сохранение сообений в файл
    db = open(DB_FILE, "w")     # открытие бд
    data = {
        "messages" : messages
    }   # создание новой бд
    json.dump(data, db) # перезапись бд
def add_message(text, sender):  # Объявим функцию, которая добавит сообщение в список
    now = datetime.datetime.now()  # импорт объекта даты сейчас
    new_message = {
        "text": text,
        "sender": sender,
        "time": now.strftime("%H:%M")
    }
    messages.append(new_message)  # Добавляем новое сообщение в список
    save_messages_to_file()

def check_numbers_of_messages():
    if len(messages)>26:
        del messages[0]
    else:
        return

def print_message(message):  # Объявляем функцию, которая будет печатать одно сообщение
    print(f"[{message['sender']}]: {message['text']} / {message['time']} ")


for message in messages:    # цикл для перебора сообщений внутри списка сообщений
    print_message(message)

#main page
@app.route("/") #ровно над предыдущей строчки сущности, к которой это относится. это аннотация
def index_page():
    return "helo, chel!"

#формат джейсон
@app.route("/get_messages")
def get_messages():
    return {'messages': messages}

@app.route("/form")
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

app.run()

