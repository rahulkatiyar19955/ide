from project import db
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from datetime import datetime

class upload_docsView(ModelView):
    column_list = {'id','user_id','subject_id','file_name','submitTime'}
    def is_accessible(self):
        if current_user.is_authenticated:
            if current_user.role == 2:
                return True
        return False

class Uploaddocs(db.Model):
    __bind_key__ = 'uploaddocs'
    __tablename__ = "uploaddocs"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), nullable=False)
    subject_id = db.Column(db.Integer, nullable=False)
    file_name = db.Column(db.String(100), nullable=False)
    uploadFile = db.Column(db.LargeBinary, nullable=False)
    submitTime = db.Column(db.DateTime, nullable=False)

    def __init__(self, user_id,file_name, uploadFile, subject_id):
        self.user_id = user_id
        self.file_name = file_name
        self.uploadFile = uploadFile
        self.subject_id = subject_id
        self.submitTime = datetime.now()

    def __repr__(self):
        return f"File('{self.id}')"

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
