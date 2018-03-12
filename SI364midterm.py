###############################
####### SETUP (OVERALL) #######
###############################

## Import statements
# Import statements
import os
from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError, IntegerField # Note that you may need to import more here! Check out examples that do what you want to figure out what.
from wtforms.validators import Required # Here, too
from flask_sqlalchemy import SQLAlchemy
from wapy.api import Wapy

wapy = Wapy('hhfenmkbxvyb9j2bzr4ms654')

## App setup code
app = Flask(__name__)
app.debug = True
app.use_reloader = True

## All app.config values
app.config['SECRET_KEY'] = 'hard to guess string from si364'
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://localhost/wyutingMidterm"
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

## Statements for db setup (and manager setup if using Manager)
db = SQLAlchemy(app)


######################################
######## HELPER FXNS (If any) ########
######################################


##################
##### MODELS #####
##################

class Name(db.Model):
    __tablename__ = "names"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64))

    def __repr__(self):
        return "{} (ID: {})".format(self.name, self.id)

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64))
    products = db.relationship('Product', backref='User')

    def __repr__(self):
        return '{username %r} | ID: {%a}' %  (self.username, self.id)

class Product(db.Model):
    __tablename__ = "products"
    product_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    product_name = db.Column(db.String(280))

    def __repr__(self):
        return '{Product ID %r} | Product Name: {%a}' %  (self.product_id, self.product_name)

class Review(db.Model):
    __tablename__ = "reviews"
    id = db.Column(db.Integer,primary_key=True)
    product_id = db.Column(db.Integer)
    #username = db.Column(db.Integer, db.ForeignKey('users.username'))
    product_name = db.Column(db.String(280))
    review = db.Column(db.String)

    def __repr__(self):
        return '{Product Name %r} | Review: {%a}' %  (self.product_name, self.review)



###################
###### FORMS ######
###################

def validate_num_entries(form,field):
    if field.data < 1 or field.data > 20:
        raise ValidationError ('Number of entries can only be within 1 and 20.')
    else:
        raise ValidationError ('Your entry should be a number.')


class NameForm(FlaskForm):
    name = StringField("Please enter your name. ",validators=[Required()])
    submit = SubmitField()

class SearchForm(FlaskForm):
    keyword = StringField("Enter the product keyword: ",validators=[Required()])
    num_entries = IntegerField("Enter how many search entries you want (at least 1 and no more than 20): ", validators=[Required(), validate_num_entries])
    submit = SubmitField()

class ProductForm(FlaskForm):
    username = StringField('Please enter your username: ', validators=[Required()])
    product_id = IntegerField("Please enter the product id: ",validators=[Required()])
    submit = SubmitField()

class UserForm(FlaskForm):
    username = StringField('Please enter your username: ', validators=[Required()])
    submit = SubmitField()

class ReviewForm(FlaskForm):
    product_id = IntegerField('Enter the item id of the product that you would like to review', validators=[Required()])
    review = StringField('Please enter your review:', validators=[Required()])
    submit = SubmitField()


#######################
###### VIEW FXNS ######
#######################

@app.route('/',methods=['GET', 'POST'])
def home():
    form = NameForm() # User should be able to enter name after name and each one will be saved, even if it's a duplicate! Sends data with GET
    if request.method == 'POST' and form.validate_on_submit():
        name = form.name.data
        newname = Name(name=name)
        db.session.add(newname)
        db.session.commit()
        return redirect(url_for('all_names'))
    return render_template('base.html',form=form)


@app.route('/names')
def all_names():
    names = Name.query.all()
    return render_template('name_example.html',names=names)

@app.route('/search')
def search():
    form = SearchForm()
    return render_template('search.html',form=form)

@app.route('/search_result', methods = ['GET', 'POST'])
def search_result():
    form = SearchForm(request.form)
    if request.method == 'POST':
        print('-------------------------')
        keyword = form.keyword.data
        print(keyword)
        num_entries = form.num_entries.data
        print(num_entries)
        products = wapy.search(keyword)[0:num_entries]
        product_list = []
        for p in products:
            product_list.append({'product_name': p.name, 'customer_rating': p.customer_rating, 'item_id': p.item_id, 'price': p.sale_price, 'description': p.short_description})
        print(product_list[0])
        return render_template('product_search_results.html', products=product_list, keyword=keyword)
    else:
        print('ERROR')
        flash('All fields are required!')
        return redirect(url_for('search'))

@app.route('/add_product', methods = ['GET', 'POST'])
def add_product():
    form = ProductForm()
    if request.method == 'POST':
        username = form.username.data
        product_id = form.product_id.data

        user = User.query.filter_by(username=username).first()
        if user:
            print("The user is in database", user.username)
        else:
            print('The user is not in database yet. Adding it to database...')
            user = User(username=username)
            db.session.add(user)
            db.session.commit()
            print('successfully added the user', user.username)

        product_name = wapy.product_lookup(str(product_id)).name
        product = Product.query.filter_by(product_id=product_id).first()
        if product:
            print('The product is in database.')
            flash('Product is already in database.')
            return redirect(url_for('add_product'))
        else:
            print('The product is not in database. Adding it to the database...')
            product = Product(product_id=product_id, user_id=user.id, product_name=product_name)
            print("successfully created product")
            db.session.add(product)
            db.session.commit()
            flash ('The product is successfully added')
            return redirect(url_for('add_product'))
    return render_template('add_product.html', form=form)

@app.route('/get_user', methods=['GET', 'POST'])
def get_user():
    form = UserForm()
    return render_template('get_user.html', form=form)

@app.route('/show_products', methods=['GET', 'POST'])
def show_products():
    username = request.args.get('username')
    user = User.query.filter_by(username=username).first()

    if user:
        products = Product.query.filter_by(user_id=user.id).all()
        product_list = []
        for p in products:
            product_list.append({'product_name': p.product_name, 'product_id': p.product_id})
        print(product_list)
        return render_template('show_products.html', products=product_list, username=username)
    else:
        print('NO USER')
        flash('User does not exist. Pleae re-enter')
        return redirect(url_for('get_user'))

@app.route('/add_review', methods=['GET', 'POST'])
def add_review():
    form = ReviewForm()
    return render_template('add_review.html', form=form)

@app.route('/show_review', methods=['GET', 'POST'])
def show_revew():
    form = ReviewForm(request.form)
    product_id = form.product_id.data
    print(product_id)
    review = form.review.data
    print(review)

    product_review = Review.query.filter_by(product_id=product_id, review=review).first()
    if product_review:
        flash('Review for the product already exist')
        return redirect(url_for('add_review'))

    try:
        print("New product review")
        product_name = wapy.product_lookup(str(product_id)).name
        print(product_name)
        product_review = Review(product_id=product_id, product_name=product_name, review=review)
        db.session.add(product_review)
        db.session.commit()
        print('successfully added the review for ', product_review.review)
        return render_template('show_review.html',product_name=product_name, review=review)
    except:
        flash("Product Id does not exist. Try something else!")
        return redirect(url_for('add_review'))


@app.route('/show_all_reviews')
def show_all_reviews():
    reviews = Review.query.all()
    return render_template('show_all_reviews.html', reviews=reviews)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404



if __name__ == '__main__':
    db.create_all() # Will create any defined models when you run the application
    app.run(use_reloader=True,debug=True) # The usual


## Code to run the application...

# Put the code to do so here!
# NOTE: Make sure you include the code you need to initialize the database structure when you run the application!
