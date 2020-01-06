from project import db
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user


class subject_listView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated:
            if current_user.role == 2:
                return True
        return False


class subjectlist(db.Model):
    __bind_key__ = 'subjectlist'
    __tablename__ = "subjectlist"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Subject('{self.id}')"

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
