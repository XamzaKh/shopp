from flask import Flask, render_template, redirect, url_for, request
import secrets
import os
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from flask_login import LoginManager, login_user, current_user, UserMixin


ALLOWED_EXTENSIONs = {'png', 'jpg', 'jpeg'}
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///electro_shop.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = 'dawkdjhfio213lasd131ldajsfko17gf'
app.config['UPLOAD_FOLDER'] = 'static/images'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'




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


@app.route('/')
def index():
    product = Product.query.all()
    return render_template('index.html', products=product)




@app.route('/product')
def product():
    return render_template('product.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    username= request.form.get('username')
    password= request.form.get('password')    
    user = User.query.filter_by(username=username,password=password).first()
    if user:
        login_user(user)
        return redirect(url_for('index'))       
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if current_user.is_anonymous:
        return redirect(url_for('index'))
    if request.method == 'POST':
        file_name = request.files.get('image')    
        filename = secure_filename(file_name.filename)
        file_name.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)) 
        product = Product(title=request.form.get('title'), body=request.form.get('body'), price=request.form.get('price'), category=request.form.get('category'),
        availability=request.form.get('availability'), image=filename)
        db.session.add(product)
        db.session.commit()    
    return render_template('add_product.html')

@app.route('/test')
def test():
    product = Product.query.all()
    return render_template('test.html', products=product)   

if __name__ == '__main__':
    app.run(debug=True)   



    