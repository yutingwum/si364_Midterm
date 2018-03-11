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



###################
###### FORMS ######
###################

def validate_num_entries(form,field):
    if str(field.data).isdigit():
        if int(str(field.data)) < 1 and int(str(field.data)) > 20:
            raise ValidationError ('Number of entries can only be within 1 and 20.')
    else:
        raise ValidationError ('Your entry should be a number.')

def validate_product_id(form,field):
    if not str(field.data).isdigit():
        raise ValidationError ('It should include only digits')



class NameForm(FlaskForm):
    name = StringField("Please enter your name. ",validators=[Required()])
    submit = SubmitField()

class SearchForm(FlaskForm):
    keyword = StringField("Enter the product keyword: ",validators=[Required()])
    num_entries = StringField("Enter how many search entries you want (at least 1 and no more than 20): ", validators=[Required(),validate_num_entries])
    submit = SubmitField()

class productForm(FlaskForm):
    product_id = StringField("Please enter the product id: ",validators=[Required(),validate_product_id])
    submit = SubmitField



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



if __name__ == '__main__':
    db.create_all() # Will create any defined models when you run the application
    app.run(use_reloader=True,debug=True) # The usual


## Code to run the application...

# Put the code to do so here!
# NOTE: Make sure you include the code you need to initialize the database structure when you run the application!
