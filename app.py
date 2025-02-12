from flask import Flask, render_template, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
import os

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'web2'
jwt = JWTManager(app)

users = [
    {"id": 1, "username": "admin", "password": "admin"}
]

@app.route('/')
def index():
    cards = [
            {'title': 'Carte 1', 'Description': 'Contenu de la carte 1','Detail':'plus'},
            {'title': 'Carte 2', 'Description': 'Contenu de la carte 2','Detail':'plus'},
            {'title': 'Carte 3', 'Description': 'Contenu de la carte 3','Detail':'plus'},
            # Ajoutez autant de cartes que nécessaire
        ]
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
            return access_token
    
    return "Invalid credentials"

@app.route('/adduser', methods=['POST'])
def adduser():
    firstname = request.form['firstname']
    name = request.form['name']
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']

    user = {"id": len(users) + 1, "firstname": firstname, "name": name, "username": username, "password": password, "email": email}
    users.append(user)

    return "User added successfully" + str(users)

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/home')
@jwt_required()
def home():
    return render_template('home.html')

app.template_folder = os.path.join(os.getcwd(), 'app/templates')
app.static_folder = os.path.join(os.getcwd(), 'app/static')


# @app.route('/card')
# def card():
#     return render_template('card.html', img='', Card_title='', Description='',Detail='')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
