from flask import Flask, Response, redirect, url_for, request, session, abort
from flask_login import LoginManager, UserMixin, \
                                login_required, login_user, logout_user 

from os import getenv 
from dotenv import load_dotenv


app = Flask(__name__)

load_dotenv('.env')


# config
app.config.update(
    DEBUG = True,
    SECRET_KEY = getenv('SECRET_KEY'),
    NAT_LOGIN = getenv('NAT_LOGIN'),
    BEN_LOGIN = getenv('BEN_LOGIN')
)

# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# silly user model
class User(UserMixin):
    def __init__(self, id):
        self.id = id
        self.name = "nat" if id == 0 else "ben"
        self.password = app.config.get(self.name.upper() + "_LOGIN")
        
    def __repr__(self):
        return "%d/%s/%s" % (self.id, self.name, self.password)


# create some users with ids 1 to 20       
users = [User(id) for id in range(0, 1)]


# some protected url
@app.route('/')
@login_required
def home():
    return Response("Hello World!")

 
# somewhere to login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']       
        if password == app.config.get(username.upper() + "_LOGIN"):
            name = username
            user = User(name)
            login_user(user, remember=True)
            return redirect(name)
        else:
            return abort(401)
    else:
        return Response('''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=password name=password>
            <p><input type=submit value=Login>
        </form>
        ''')


# somewhere to logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return Response('<p>Logged out</p>')


# handle login failed
@app.errorhandler(401)
def page_not_found(e):
    return Response('<p>Login failed</p>')
    
    
# callback to reload the user object        
@login_manager.user_loader
def load_user(userid):
    return User(userid)
    

if __name__ == "__main__":
    app.run()
