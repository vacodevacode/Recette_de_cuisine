from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

db = client["recette_cuisine"]

users = db["users"]
recipes = db["recipes"]

def database_create():
    if users.count_documents({}) == 0:
        users.insert_many([
            {"username": "user1", "password": "hashed_password1", "token": "token1"},
            {"username": "user2", "password": "hashed_password2", "token": "token2"},
            {"username": "user3", "password": "hashed_password3", "token": "token3"},
        ])

    if recipes.count_documents({}) == 0:
        recipes.insert_many([
            {"title": "Pâtes Carbonara", "description": "Recette italienne traditionnelle avec œufs, pecorino et pancetta.", "by_user": "user1", "vote": 5},
            {"title": "Salade César", "description": "Laitue romaine, croûtons, parmesan et sauce César maison.", "by_user": "user2", "vote": 4},
            {"title": "Tarte au citron", "description": "Une tarte acidulée avec une crème onctueuse et une pâte sablée.", "by_user": "user3", "vote": 5},
        ])

database_create()