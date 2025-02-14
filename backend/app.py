from flask import Flask, request, render_template, redirect, url_for, session
from flask_bcrypt import Bcrypt
from backend.models import users, recipes
import os
from pymongo import MongoClient
from backend.models import client

app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), '../frontend/templates'),
    static_folder=os.path.join(os.path.dirname(__file__), '../frontend/static')
)

app.config['SECRET_KEY'] = 'your-secret-key'
bcrypt = Bcrypt(app)

#Doushdi
MongoClient('mongodb://localhost:27017/')
db = client["recette_cuisine"]
collection = db['recipes']

@app.route('/search', methods=['GET'])
def search_recipes():
    query = request.args.get('q', '')

    if not query:
        return "Aucun terme de recherche fourni", 400

    search_filter = {"$or": [
        {"title": {"$regex": query, "$options": "i"}},
        {"description": {"$regex": query, "$options": "i"}}
    ]}

    results = collection.find(search_filter, {"_id": 0})

    response_text = ""
    for recipe in results:
        response_text += f"📝 {recipe['title']}\n{recipe['description']}\n Score: {recipe['vote']}\n\n"

    return response_text if response_text else "Aucune recette trouvée."

@app.route('/filter', methods=['GET'])
def filter_recipes():
    category = request.args.get('category', '').strip()

    if not category:
        return "Aucune catégorie sélectionnée.", 400

    search_filter = {"title": {"$regex": category, "$options": "i"}}
    results = collection.find(search_filter, {"_id": 0})

    response_text = ""
    for recipe in results:
        response_text += f"📝 {recipe['title']}\n{recipe['description']}\n Score: {recipe['vote']}\n\n"

    return response_text if response_text else f"Aucune recette trouvée pour la catégorie '{category}'."

@app.route('/')
def home():
    # Récupérer toutes les recettes depuis la base de données
    cards = recipes.find()
    return render_template('welcome.html', cards=cards)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if users.find_one({"username": username}):
            return render_template('register.html', error="Ce nom d'utilisateur existe déjà.")

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        users.insert_one({"username": username, "password": hashed_password})

        return redirect(url_for('home'))  # Redirection après inscription

    return render_template('register.html')

# Ajout de la route '/adduser' pour l'inscription (si nécessaire)
@app.route('/adduser', methods=['POST'])
def add_user():
    return register()  # Appelle directement la fonction register()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = users.find_one({"username": username})
        if user and bcrypt.check_password_hash(user['password'], password):
            session['username'] = username  # Stocke l'utilisateur en session
            return redirect(url_for('protected'))  # Redirection après connexion

        return render_template('login.html', error="Identifiants incorrects.")

    return render_template('login.html')

@app.route('/protected')
def protected():
    if 'username' not in session:
        return redirect(url_for('login'))  # Redirige vers login si pas connecté
    
    user_recipes = recipes.find({"by_user": session['username']})
    return render_template('protected.html', username=session['username'], recipes=user_recipes)

@app.route('/logout')
def logout():
    session.pop('username', None)  # Déconnecte l'utilisateur
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
