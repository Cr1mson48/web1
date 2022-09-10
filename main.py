import csv
import os
import subprocess as sp
from data import db_session
from data.reviews import Listings
from data.task import Tasks
from data.api_account import Api_account
from data.users import User
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email_validate import validate
from flask import Flask, render_template, url_for, redirect, request, make_response
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from forms.login_user import LoginForm
from forms.order import OrderForm
from forms.add_task import Addtask
from forms.reg_user import RegisterForm
from forms.add_api import APIForm
from forms.reviews import ReviewsForm
from redis import Redis
import rq
from rq.registry import ScheduledJobRegistry
from funs import pcheck
from smtplib import SMTP

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


from_email = 'wqisup@gmail.com'
password = 'Yq5-4DY-eJw-CMq'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


def main():
    db_session.global_init("db/data.db")
    app.task_queue_mexc = rq.Queue('mexc', connection=Redis(host="localhost", port="6379"))
    app.run()



@app.route('/')
@app.route('/index')
def index():
    db_sess = db_session.create_session()
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        msg = MIMEMultipart()
        server = SMTP('smtp.gmail.com: 587')
        if validate(form.email.data):
            if form.password.data != form.password_again.data:
                return render_template('register.html', title='Регистрация',
                                       form=form,
                                       message="Пароли не совпадают")

            error = pcheck(form.password.data)
            if not error:
                return render_template('register.html', title='Регистрация',
                                       form=form,
                                       message=error)
            db_sess = db_session.create_session()
            if db_sess.query(User).filter(User.email == form.email.data).first():
                return render_template('register.html', title='Регистрация',
                                       form=form,
                                       message="Такой пользователь уже есть")
            user = User(
                name=form.name.data,
                email=form.email.data,
            )
            user.set_password(form.password.data)
            db_sess.add(user)
            db_sess.commit()
            message = 'Вы зарегистрировались'
            return redirect('/login')
        else:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такого адреса не существует")
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/example.php')
def phpexample():
    out = sp.run(["php", "example.php"], stdout=sp.PIPE)
    return out.stdout



@app.route('/add', methods=['GET', 'POST'])
def add():
    if current_user.is_authenticated == False:
        return redirect('/login')

    form = Addtask()
    if request.method == "POST":
        db_sess = db_session.create_session()
        name = request.form.get('select-form1')
        buy = request.form.get('select-form2')
        data = request.form.get('data')
        print(form.remember_me.data)

        task_api = db_sess.query(Api_account).filter(Api_account.name == name).all()
        for i in task_api:
            api = i.api
            secret = i.secret
        print(api, secret)

        current_user.launch_task_mexc(id_users=current_user.id, name1=name, ticker=form.ticker.data,
                         price=form.price.data, price_buy=form.price_buy.data, buy=buy, data=data, time=form.time.data, api=api, secret=secret )
        db_sess.commit()
        #add_task = Tasks(id_users=current_user.id, name=name, ticker=form.ticker.data,
        #                 price=form.price.data, sell=if_sell, buy=buy, data=data, time=form.time.data)

        #try:
        #    db_sess.add(add_task)
        #    db_sess.commit()
        #    return redirect('/')
        #except:
        #    return "При добавление задания произошла ошибка"


    market = ["Market", "Limit"]
    db_sess = db_session.create_session()
    acc = db_sess.query(Api_account).filter(Api_account.id == current_user.id).all()
    return render_template('add.html', acc=acc, market=market, form=form)



@app.route('/api', methods=['GET', 'POST'])
def api():
    if current_user.is_authenticated == False:
        return redirect('/login')
    db_sess = db_session.create_session()
    # print(current_user.email)
    form = APIForm()
    if form.validate_on_submit():
        select = request.form.get('select-form')
        print(select, form.name_account.data, form.apiKey.data, form.secretKey.data, form.PassPhrase.data)
        db_sess = db_session.create_session()
        api_acc = Api_account(id=current_user.id, market=select, name=form.name_account.data,
                              api=form.apiKey.data, secret=form.secretKey.data,
                              passPhrase=form.PassPhrase.data)
        try:
            db_sess.add(api_acc)
            db_sess.commit()
            return redirect('/')
        except Exception as e:
            print(e)
            return "При добавление api произошла ошибка"



    list = ["Binance", "ByBit", "Kucoin", "Mexc", "OKX"]
    db_sess = db_session.create_session()
    return render_template('api.html', option=list, form=form)


@app.route('/create-listing', methods=['GET', 'POST'])
def create():
    if request.method == "POST":
        db_sess = db_session.create_session()
        title = request.form['title']
        text = request.form['text']
        data = request.form['data']

        listing = Listings(title=title, text=text, time=data)

        try:
            db_sess.add(listing)
            db_sess.commit()
            return redirect('/')
        except:
            return "При добавление листинга произошла ошибка"

    return render_template('create-liting.html')


@app.route('/tasks', methods=['GET', 'POST'])
def tasks():
    db_sess = db_session.create_session()
    tasks = db_sess.query(Tasks).filter(Tasks.id_users == current_user.id).order_by(Tasks.created_date).all()
    return render_template('tasks.html', tasks=tasks)


@app.route("/logout")
def logout():
    logout_user()
    return redirect("/index")


if __name__ == '__main__':
    main()
