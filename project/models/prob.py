from project import db


class Prob(db.Model):
    __bind_key__ = 'problems'
    __tablename__ = "Prob"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True, nullable=False)
    difficulty = db.Column(db.String(10), nullable=False)
    content = db.Column(db.Text, nullable=False)
    input1 = db.Column(db.Text, nullable=False)
    output1 = db.Column(db.Text, nullable=False)
    constraint = db.Column(db.Text, nullable=False)
    test_case1 = db.Column(db.Text, nullable=False)
    explanation = db.Column(db.Text, nullable=False)

    def __init__(self, title, difficulty, content, input1, output1, constraint, test_case1, explanation):
        self.title = title
        self.difficulty = difficulty
        self.content = content
        self.input1 = input1
        self.output1 = output1
        self.constraint = constraint
        self.test_case1 = test_case1
        self.explanation = explanation

    @classmethod
    def get_from_id(cls, problem_id):
        return cls.query.filter_by(id=problem_id).first()

    def __repr__(self):
        return f"Prob('{self.title}','{self.difficulty}',{self.content})"

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
