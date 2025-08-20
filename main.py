from flask import Flask,render_template,request,session,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,logout_user,login_manager,LoginManager
from flask_login import login_required,current_user

import datetime


#my db connection
local_server=True
app = Flask(__name__)
app.secret_key='sakshishinde'

#unique user access
login_manager=LoginManager(app)
login_manager.login_view='login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



#app.config['SQLALCHEMY_DATABASE_URL']='mysql://username:password@localhost/database_table_name'

app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:root123@localhost/dbms'

# print("Flask App Configuration:")
# for key, value in app.config.items():
#     print(f"{key}: {value}")

db=SQLAlchemy(app)

#here we will create db models 
class Test(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(20))
    email=db.Column(db.String(30))

class User(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(50))
    email=db.Column(db.String(50),unique=True)
    password=db.Column(db.String(1000))

class Sponsor(db.Model): # Updated Sponsor model to match database schema
    SponsorID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(255), nullable=False)
    Address = db.Column(db.String(255))
    Email = db.Column(db.String(255))
    C_Phone = db.Column(db.String(20))
    ContactPerson = db.Column(db.String(255))

class Event(db.Model):  # Updated Event model to match your table
    EventID = db.Column(db.Integer, primary_key=True)  # Renamed to match database
    Name = db.Column(db.String(255), nullable=False)  # Renamed to match database
    Description = db.Column(db.Text)  # Renamed to match database
    Venue = db.Column(db.String(255))  # Renamed to match database
    EventDate = db.Column(db.Date)  # Renamed to match databases

#endpoints and run the functions
@app.route('/sponsor')
@login_required
def sponsor():
    if not User.is_authenticated:
        return render_template('login.html')
    else:
        return render_template('sponsor.html',username=current_user.username)
    return render_template('sponsor.html')

@app.route('/event')
@login_required
def event():
    today = datetime.date.today()
    ongoing_events = Event.query.filter(Event.EventDate == today).all()
    upcoming_events = Event.query.filter(Event.EventDate > today).order_by(Event.EventDate).all()
    past_events = Event.query.filter(Event.EventDate < today).order_by(Event.EventDate.desc()).all()
    return render_template('event.html', ongoing_events=ongoing_events, upcoming_events=upcoming_events, past_events=past_events)

@app.route('/package')
def package():
    return render_template('package.html')

@app.route('/payment')
def payment():
    return render_template('payment.html')

@app.route('/agreement')
def agreement():
    return render_template('agreement.html')

@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method == "POST":
        username=request.form.get('username')
        email=request.form.get('email')
        password=request.form.get('password')
        user=User.query.filter_by(email=email).first()
        if user:
            flash("Email already exists","warning")
            return render_template('signup.html')
        encpassword=generate_password_hash(password)
        newuser=User(username=username,email=email,password=encpassword)
        db.session.add(newuser)
        db.session.commit()
        flash("Signup success, Please Login","success")
        return render_template('login.html')


    return render_template('signup.html')

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == "POST":
        email=request.form.get('email')
        password=request.form.get('password')
        user=User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password,password):
            login_user(user)
            flash("Login success","primary")
            return redirect(url_for('index'))
        else:
            flash("Invalid credentials","danger")
            return render_template('login.html')

        
    return render_template('login.html')

@app.route('/logout')
@login_required
def logOut():
    logout_user()
    flash("LogOut Successfully.","warning")
    return redirect(url_for('login'))



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/test')
def test():
    try:
        Test.query.all()
        return 'My database is connected'
    except:
        return 'My database is not connected'
    



app.run(debug=True)

#username=current_user.username