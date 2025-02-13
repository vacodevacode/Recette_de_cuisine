from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient("mongodb://localhost:27017/")
db = client["recette_cuisine"]

users = db["users"]
recipes = db["recipes"]

def database_create():
    if users.count_documents({}) == 0:
        users.insert_many([
            {"username": "user1", "password": "hashed_password1"},
            {"username": "user2", "password": "hashed_password2"},
            {"username": "user3", "password": "hashed_password3"},
        ])

    if recipes.count_documents({}) == 0:
        recipes.insert_many([
            {"title": "Pâtes Carbonara", "description": "Recette italienne traditionnelle.", "by_user": "user1", "vote": 5},
            {"title": "Salade César", "description": "Laitue romaine, croûtons, parmesan.", "by_user": "user2", "vote": 4},
            {"title": "Tarte au citron", "description": "Tarte acidulée avec crème onctueuse.", "by_user": "user3", "vote": 5},
        ])

database_create()
