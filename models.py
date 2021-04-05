from flask_sqlalchemy import SQLAlchemy
from shop import login_manager
from flask_login import UserMixin
db = SQLAlchemy()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(), nullable=False)
    def __repr__(self): 
        return self.username  


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(), nullable=False)
    body = db.Column(db.Text(), nullable=False)
    price = db.Column(db.Integer(), nullable=False)
    category = db.Column(db.String(), nullable=False, default='Категория')
    availability = db.Column(db.String(), nullable=False, default='Есть в наличии')
    image = db.Column(db.String(), nullable=False)
    
    def __repr__(self): 
        return self.title
