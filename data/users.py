import datetime
import sqlalchemy
from redis import Redis
import rq
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from data.task import Tasks
from data import db_session
from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

db_session.global_init("db/data.db")
db_sess = db_session.create_session()



class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)

    task_queue_mexc = rq.Queue('mexc', connection=Redis(host="localhost", port="6379"))

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def launch_task_mexc(self, name1, ticker, price, price_buy, buy, data, time, api, secret, *args, **kwargs):
        try:
            task = Tasks(id_users=current_user.id, name=name1, ticker=ticker,
                         price=price, price_buy=price_buy, buy=buy, data=data, time=time)
            db_sess.add(task)
            db_sess.commit()
            print('Добавили в бд')
        except Exception as e:
            print(e)
        rq_job = current_user.task_queue_mexc.enqueue('listing_mexc.mexc_listing', api=api, secret=secret)
        print('Выполнилось')
        #task = Tasks(id_users=current_user.id, name=name1, ticker=form.ticker.data,
        #             price=form.price.data, sell=if_sell, buy=buy, data=data, time=form.time.data)
        return task

    def get_tasks_in_progress(self):
        return Tasks.query.filter_by(user=self, complete=False).all()

    def get_task_in_progress(self, name):
        return Tasks.query.filter_by(name=name, user=self,
                                    complete=False).first()
