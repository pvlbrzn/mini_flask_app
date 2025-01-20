from flask import Flask, render_template
from datetime import datetime

'''Создаем объект на основе класса Flask.
В конструктор передаем имя файла, который будет 
являться основным'''
app = Flask(__name__)


@app.route('/')  # декоратор для отслеживания URL главной страницы
@app.route('/home')
def index():
    """Функция для вывода контента на странице"""
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/contacts')
def contacts():
    return render_template("contacts.html")


@app.route("/hello/")
@app.route("/hello/<name>")
def hello(name=None):
    if not name:
        name = "Гость"
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return render_template("hello.html", name=name, current_time=current_time)


if __name__ == "__main__":
    app.run(debug=True)  # Параметр debug=True для отслеживания ошибок
