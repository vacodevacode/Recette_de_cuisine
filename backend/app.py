from flask import Flask, render_template, request, redirect, url_for
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, set_access_cookies
import os

from pymongo import MongoClient
from backend.models import client 

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'web2'
jwt = JWTManager(app)

users = [
    {"id": 1, "username": "admin", "password": "admin"}
]
MongoClient('mongodb://localhost:27017/')
db = client["recette_cuisine"]
collection = db['recipes']


@app.route('/')
def index():
    cards = list(collection.find())
    return render_template('welcome.html',cards=cards)



#NE PAS TOUCHER URL DE TEST:
@app.route('/card')
def card():
    cards = list(collection.find())
    # [
    #         {'title': 'Carte 1', 'Description': 'Contenu de la carte 1','Detail':'plus'},
    #         {'title': 'Carte 2', 'Description': 'Contenu de la carte 2','Detail':'plus'},
    #         {'title': 'Carte 3', 'Description': 'Contenu de la carte 3','Detail':'plus'},
    #         # Ajoutez autant de cartes que nécessaire
    #     ]
    return render_template('index.html', cards=cards)


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
