import bcrypt
import re
from pymongo import MongoClient
from bson.objectid import ObjectId  # For converting string to ObjectId

class Database:
    def __init__(self):
        uri = "mongodb+srv://Alexis:gMggzxyJ50RwhRb5@reservationcluster.wq3eeod.mongodb.net/?retryWrites=true&w=majority&appName=ReservationCluster"
        self.client = MongoClient(uri)
        self.db = self.client["airbnb"]
        self.guests = self.db["guests"]
        self.listings = self.db["listings"]
        self.reservations = self.db["reservations"]

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

    def get_listing_info(self, listing_id):
        try:
            result = self.listings.find_one({"_id": ObjectId(listing_id)})
        except Exception:
            result = self.listings.find_one({"host.host_id": listing_id})

        if result:
            return {
                "name": result.get("name", "N/A"),
                "price": result.get("price", "N/A"),
            }

        return None

    def save_reservation(self, guest_email, listing_id, listing_name, guest_count, arrival_date, leaving_date, total_cost):
        reservation = {
            "guest_email": guest_email,
            "listing_id": listing_id,
            "listing_name": listing_name,
            "guest_count": guest_count,
            "arrival_date": arrival_date,
            "leaving_date": leaving_date,
            "total_cost": total_cost,
            "status": "pending"
        }
        self.db.reservations.insert_one(reservation)


    def get_reservations_for_guest(self, guest_email):
        """Fetch all reservations for the logged-in guest"""
        return list(self.reservations.find({"guest_email": guest_email}))

    def cancel_reservation(self, reservation_id):
        """Delete reservation by its ObjectId"""
        self.reservations.delete_one({"_id": ObjectId(reservation_id)})