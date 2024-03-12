from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True, unique=True)
    address = db.Column(db.String(50),index=True, unique=True)
    salary = db.Column(db.Integer, nullable=False)
