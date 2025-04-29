import requests

BASE_URL = "http://localhost:5173/api"

# ---------- AUTHENTICATION ----------

def register_guest(name, email, password):
    response = requests.post(f"{BASE_URL}/guests/register", json={
        "name": name,
        "email": email,
        "password": password
    })
    return response.json()

def login_guest(email, password):
    response = requests.post(f"{BASE_URL}/guests/login", json={
        "email": email,
        "password": password
    })
    return response.json()

def logout_guest(token):
    # Optional if using token-based sessions
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{BASE_URL}/guests/logout", headers=headers)
    return response.json()

# ---------- LISTING SEARCH ----------

def search_listings(criteria):
    response = requests.get(f"{BASE_URL}/listings/search", params=criteria)
    return response.json()

def get_listing_details(listing_id):
    response = requests.get(f"{BASE_URL}/listings/{listing_id}")
    return response.json()

# ---------- RESERVATIONS ----------

def make_reservation(token, listing_id, start_date, end_date):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{BASE_URL}/reservations", json={
        "listingId": listing_id,
        "startDate": start_date,
        "endDate": end_date
    }, headers=headers)
    return response.json()

def get_guest_reservations(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/reservations/guest", headers=headers)
    return response.json()

def cancel_reservation(token, reservation_id):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.patch(f"{BASE_URL}/reservations/{reservation_id}/cancel", headers=headers)
    return response.json()
