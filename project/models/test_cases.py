from project import db
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

class testCaseView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated:
            if current_user.role == 2:
                return True
        return False

class Testcases(db.Model):
    __bind_key__ = 'testcases'
    __tablename__ = "Testcases"
    id = db.Column(db.Integer, primary_key=True)
    problem_id = db.Column(db.Integer, db.ForeignKey('Prob.id'))
    input = db.Column(db.Text, nullable=False)
    output = db.Column(db.Text, nullable=False)
    timeout = db.Column(db.Integer, nullable=False)

    def __init__(self, input1, output, problem_id, timeout):
        self.input = input1
        self.output = output
        self.problem_id = problem_id
        self.timeout = timeout

    @classmethod
    def get_from_project_id(cls, problem_id):
        return cls.query.filter_by(problem_id=problem_id)

    def __repr__(self):
        return f"Testcase('{self.id}')"

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
