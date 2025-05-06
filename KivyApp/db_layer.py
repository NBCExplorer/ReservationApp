import bcrypt
from pymongo import MongoClient

class Database:
    def __init__(self):
        uri = "mongodb+srv://Alexis:gMggzxyJ50RwhRb5@reservationcluster.wq3eeod.mongodb.net/?retryWrites=true&w=majority&appName=ReservationCluster"
        self.client = MongoClient(uri)
        self.db = self.client["airbnb"]
        self.guests = self.db["guests"]

    def validate_guest_login(self, email, password):
        user = self.guests.find_one({"email": email})
        if user and bcrypt.checkpw(password.encode(), user["password"]):
            return True
        return False

    def register_guest(self, first_name, last_name, email, password):
        if self.guests.find_one({"email": email}):
            return False  # Email already exists

        hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        self.guests.insert_one({
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": hashed_pw
        })
        return True
