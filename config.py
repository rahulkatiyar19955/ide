USERNAME = 'rahulkatiyar19955@gmail.comcon1'
password = ''
SQLALCHEMY_DATABASE_URI = "sqlite:///user.db"
SQLALCHEMY_BINDS = {'codebase': "sqlite:///cb.db",
                    'testcases': "sqlite:///tc.db",
                    'problems': "sqlite:///prob.db"}
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = 'MY_SECRET_KEY'
