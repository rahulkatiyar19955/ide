from project import db


class CodeBase(db.Model):
    __tablename__ = "CodeBase"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True, nullable=False)
    difficulty = db.Column(db.String(10), nullable=False)
    num_of_testcases = db.Column(db.Integer)

    def __init__(self, title, difficulty, num_of_testcases):
        self.title = title
        self.difficulty = difficulty
        self.num_of_testcases = num_of_testcases

    def __repr__(self):
        return f"Title('{self.title}','{self.difficulty}')"
