from app import db
from sqlalchemy.dialects.postgresql import JSON


class Result(db.Model):
    __tablename__ = 'results'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String())
    result_all = db.Column(JSON)
    result_no_stop_words = db.Column(JSON)

    def __init__(self, url, result_all, result_no_stop_words, id):
        self.url = url
        self.result_all = result_all
        self.result_no_stop_words = result_no_stop_words
        self.id = id

    def __repr__(self):
        return '<id {} url {}>'.format(self.id, self.url)

    def __eq__(self, other):
        return f"{self.url}" == f"{other.url}"

    def __hash__(self):
        return hash(self.url)
