USERNAME = 'rahulkatiyar19955@gmail.com'
PASSWORD = '9784331618'
SQLALCHEMY_DATABASE_URI = "sqlite:///user.db"
# SQLALCHEMY_DATABASE_URI = "mysql+pymysql://admin:amazondata@database1.calnggnlssfl.us-east-1.rds.amazonaws.com
# /ide_database" SQLALCHEMY_BINDS = {'codebase':
# "mysql+pymysql://admin:amazondata@database1.calnggnlssfl.us-east-1.rds.amazonaws.com/ide_database", 'testcases':
# "mysql+pymysql://admin:amazondata@database1.calnggnlssfl.us-east-1.rds.amazonaws.com/ide_database", 'problems':
# "mysql+pymysql://admin:amazondata@database1.calnggnlssfl.us-east-1.rds.amazonaws.com/ide_database"}
SQLALCHEMY_BINDS = {'codebase': "sqlite:///cb.db",
                    'testcases': "sqlite:///tc.db",
                    'subjectlist': "sqlite:///subjects.db",
                    'uploaddocs': "sqlite:///upload.db",
                    'problems': "sqlite:///prob.db"}
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = 'MY_SECRET_KEY'
