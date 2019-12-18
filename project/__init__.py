from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

application = Flask(__name__)
# mysql+pymysql://<db_user>:<db_password>@<endpoint>/<db_url>
# mysql+pymysql://admin:HjDfCtUBkLhWHX1LKda0@database1.calnggnlssfl.us-east-1.rds.amazonaws.com
# amazondata
# admin HjDfCtUBkLhWHX1LKda0 database1.calnggnlssfl.us-east-1.rds.amazonaws.com
# application.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://admin:amazondata@database1.calnggnlssfl.us-east-1.rds.amazonaws.com/database1"
application.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"
application.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
application.config['SECRET_KEY'] = 'MY_SECRET_KEY'
db = SQLAlchemy(application)
bcrypt = Bcrypt(application)
login_manager = LoginManager(application)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
application.config['Mail_SERVER'] = 'smtp.gmail.com'
application.config['MAIL_PORT'] = 587
application.config['MAIL_USE_TLS'] = True
application.config['MAIL_USE_SSL'] = False
application.config['MAIL_USERNAME'] = 'rahulkatiyar19955@gmail.com'
application.config['MAIL_PASSWORD'] = ' '
mail = Mail(application)

from project.recipe import routes
