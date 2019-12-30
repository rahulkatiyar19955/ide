from project import db
from project.models.user import UserModel
from datetime import datetime
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

class codeBaseView(ModelView):
    column_list = ['user_id','Submit_time','code_file','problem_id']
    column_filters = ['user_id','problem_id']
    can_view_details = True
    def is_accessible(self):
        if current_user.is_authenticated:
            if current_user.role == 2:
                return True
        return False

class CodeBase(db.Model):
    __bind_key__ = 'codebase'
    __tablename__ = "CodeBase"
    id = db.Column(db.Integer, primary_key=True)
    Submit_time = db.Column(db.DateTime, nullable=False)
    code_file = db.Column(db.LargeBinary, nullable=False)
    problem_id = db.Column(db.Integer, db.ForeignKey('Prob.id'))
    # problem = db.relationship("Prob")
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # user = db.relationship("UserModel")

    def __init__(self, code_file, problem_id, user_id):
        self.code_file = code_file
        self.problem_id = problem_id
        self.user_id = user_id
        # self.user = user
        self.Submit_time = datetime.now()
        # self.problem = problem

    def __repr__(self):
        return f"Title('{self.title}','{self.difficulty}')"

    @classmethod
    def get_by_id(cls,code_id):
        return cls.query.filter_by(id=code_id).first()

    @classmethod
    def is_already_available(cls, problem_id, user_id):
        if cls.query.filter_by(problem_id=problem_id, user_id=user_id).first():
            return True
        else:
            return False

    def replace_existing(self,code_file,problem_id,user_id):
        temp_code = CodeBase.query.filter_by(problem_id=problem_id, user_id=user_id).first()
        if temp_code:
            temp_code = self
            db.session.commit()
        else:
            db.session.add(self)
            db.session.commit()

    def update_to_db(self):
        if self is not None:
            db.session.add(self)
        else:
            db.session.commit()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
