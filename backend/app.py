from flask import Flask, render_template, request, redirect, url_for
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, set_access_cookies
import os

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'web2'
jwt = JWTManager(app)

users = [
    {"id": 1, "username": "admin", "password": "admin"}
]

@app.route('/')
def index():
    return render_template('signin.html')

@app.route('/signin')
def signin():
    return render_template('signin.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    for user in users:
        if user['username'] == username and user['password'] == password:
            access_token = create_access_token(identity=username)
            response = redirect(url_for('home'))
            set_access_cookies(response, access_token)  
            return response

    return "Invalid credentials", 401

@app.route('/adduser', methods=['POST'])
def adduser():
    firstname = request.form['firstname']
    name = request.form['name']
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']

    user = {"id": len(users) + 1, "firstname": firstname, "name": name, "username": username, "password": password, "email": email}
    users.append(user)

    return redirect(url_for('signin'))

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/home')
@jwt_required()
def home():
    return render_template('home.html')

app.template_folder = os.path.join(os.getcwd(), 'frontend/templates')
app.static_folder = os.path.join(os.getcwd(), 'frontend/static')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
