from flask import Flask
import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec
from flask_login import LoginManager, login_user, login_required, logout_user

database = dec.declarative_base()
__factory = None
# путь относительно main.py
DB_PATH = 'website/db/mars_explorer.sqlite'


def db_init(db_file=DB_PATH):
    global __factory

    if __factory:
        return

    db_file = db_file.strip()
    if not db_file:
        raise Exception('Необходимо указать файл базы данных.')

    conn_str = f'sqlite:///{db_file}?check_same_thread=False'
    print(f'Подключение к базе данных по адресу {conn_str}')

    engine = sa.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    from .models import __all_models

    database.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

    db_init()

    login_manager = LoginManager()
    login_manager.init_app(app)

    from .models import users

    @login_manager.user_loader
    def load_user(user_id):
        db_sess = create_session()
        return db_sess.query(users.User).get(user_id)

    from .jobs_api import jobs_blueprint
    app.register_blueprint(jobs_blueprint)

    return app
