from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'  # Для сообщений flash
db = SQLAlchemy(app)


# Модель
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"


@app.route('/')
@app.route('/home')
def index():
    """Главная страница"""
    return render_template("index.html")


@app.route('/about')
def about():
    """Страница 'О нас'"""
    return render_template("about.html")


@app.route('/contacts')
def contacts():
    """Страница контактов"""
    return render_template("contacts.html")


@app.route("/hello/")
@app.route("/hello/<name>")
def hello(name=None):
    """Приветственная страница"""
    if not name:
        name = "Гость"
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return render_template("hello.html", name=name, current_time=current_time)


@app.route('/users')
def user():
    """Вывод всех пользователей"""
    users = User.query.all()
    return render_template("users.html", users=users)


@app.route('/add', methods=['POST'])
def add_user():
    """Добавление пользователя"""
    username = request.form.get('username')
    email = request.form.get('email')

    if not username or not email:
        flash("Имя пользователя и email обязательны!", "error")
        return redirect(url_for('user'))

    # Проверка уникальности email
    if User.query.filter_by(email=email).first():
        flash("Пользователь с таким email уже существует!", "error")
        return redirect(url_for('user'))

    try:
        new_user = User(username=username, email=email)
        db.session.add(new_user)
        db.session.commit()
        flash(f"Пользователь {username} успешно добавлен!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Ошибка при добавлении пользователя: {str(e)}", "error")

    return redirect(url_for('user'))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Создание таблиц в базе данных
    app.run(debug=True)
