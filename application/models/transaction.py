from application.extensions import db
from datetime import datetime


class Transaction(db.Model):
    _tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    amount = db.Column(db.Float)
    status = db.Column(db.Integer)
    plan = db.Column(db.Integer, db.ForeignKey('plans.id'))
    owner = db.Column(db.Integer, db.ForeignKey('users.id'))
