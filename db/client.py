from pymongo import MongoClient


db_client = MongoClient(
    "mongodb+srv://test:test@cluster0.ieup57p.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0").test

print("conexion exitosa")
