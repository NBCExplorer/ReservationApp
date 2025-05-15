from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from db_layer import Database
from bson.decimal128 import Decimal128

db = Database()

Builder.load_file('ui.kv')


class WelcomeScreen(Screen):
    pass


class LoginScreen(Screen):
    def login_guest(self):
        email = self.ids.email_input.text
        password = self.ids.password_input.text
        if db.validate_guest_login(email, password):
            self.manager.current = "dashboard"
        else:
            self.ids.login_status.text = "Login failed. Try again."

    def on_pre_leave(self):
        self.ids.email_input.text = ""
        self.ids.password_input.text = ""
        self.ids.login_status.text = ""



class RegisterScreen(Screen):
    def register_guest(self):
        first = self.ids.reg_firstname_input.text
        last = self.ids.reg_lastname_input.text
        email = self.ids.reg_email_input.text
        password = self.ids.reg_password_input.text
        confirm_password = self.ids.reg_confirm_password_input.text

        if not (first and last and email and password and confirm_password):
            self.ids.register_status.text = "Please fill in all fields."
            return

        if password != confirm_password:
            self.ids.register_status.text = "Passwords do not match."
            return

        if db.register_guest(first, last, email, password):
            self.manager.current = "login"
        else:
            self.ids.register_status.text = "Email already exists."

    def on_pre_leave(self):
        self.ids.reg_firstname_input.text = ""
        self.ids.reg_lastname_input.text = ""
        self.ids.reg_email_input.text = ""
        self.ids.reg_password_input.text = ""
        self.ids.reg_confirm_password_input.text = ""
        self.ids.register_status.text = ""



class DashboardScreen(Screen):
    def search_listing(self):
        listing_id = self.ids.host_id_input.text.strip()
        info = db.get_listing_info(listing_id)
        if info:
            display = (
                f"Listing Found!\n"
                f"Name: {info['name']}\n"
                f"Price: {info['price']}"
            )
            self.ids.dashboard_status.text = display
            self.ids.availability_button.disabled = False
            self.ids.availability_button.opacity = 1
        else:
            self.ids.dashboard_status.text = "Listing not found. Please check the ID."
            self.ids.availability_button.disabled = True
            self.ids.availability_button.opacity = 0

    def go_to_reservation(self):
        self.manager.current = "reservation"

    def go_to_my_reservations(self):
        self.manager.current = "my_reservations"


class ReservationScreen(Screen):
    def confirm_reservation(self):
        guest_email = self.manager.get_screen('login').ids.email_input.text
        listing_id = self.manager.get_screen('dashboard').ids.host_id_input.text.strip()
        guest_count = self.ids.guest_count_input.text
        arrival_date = self.ids.arrival_date_input.text
        leaving_date = self.ids.leaving_date_input.text

        if not all([guest_email, listing_id, guest_count, arrival_date, leaving_date]):
            self.ids.reservation_status.text = "Please fill in all fields."
            return

        listing_info = db.get_listing_info(listing_id)
        if not listing_info:
            self.ids.reservation_status.text = "Listing not found."
            return

        try:
            guest_count_int = int(guest_count)
        except ValueError:
            self.ids.reservation_status.text = "Invalid number of guests."
            return

        price_raw = listing_info.get("price", 0)
        price = float(price_raw.to_decimal()) if isinstance(price_raw, Decimal128) else float(price_raw)
        total_cost = price * guest_count_int

        try:
            db.save_reservation(
                guest_email=guest_email,
                listing_id=listing_id,
                listing_name=listing_info.get("name", "Unknown"),
                guest_count=guest_count_int,
                arrival_date=arrival_date,
                leaving_date=leaving_date,
                total_cost=total_cost
            )
            self.ids.reservation_status.text = "Reservation saved successfully!"
        except Exception as e:
            self.ids.reservation_status.text = f"Error saving reservation: {str(e)}"

    def on_leave(self):
        self.ids.guest_count_input.text = ""
        self.ids.arrival_date_input.text = ""
        self.ids.leaving_date_input.text = ""
        self.ids.reservation_status.text = ""



class MyReservationsScreen(Screen):
    user_email = ""

    def on_enter(self):
        self.user_email = self.manager.get_screen("login").ids.email_input.text
        self.load_reservations()

    def load_reservations(self):
        container = self.ids.reservations_container
        container.clear_widgets()

        reservations = db.get_reservations_for_guest(self.user_email)

        if not reservations:
            container.add_widget(Label(text="No reservations found."))
            return

        for res in reservations:
            box = BoxLayout(orientation="vertical", size_hint_y=None, height=140)
            box.add_widget(Label(text=f"Listing: {res.get('listing_name', 'Unknown')}"))
            box.add_widget(Label(text=f"Guests: {res['guest_count']}"))
            box.add_widget(Label(text=f"Arrival: {res['arrival_date']}"))
            box.add_widget(Label(text=f"Leaving: {res['leaving_date']}"))
            box.add_widget(Label(text=f"Total Cost: ${res.get('total_cost', 0):.2f}"))
            box.add_widget(Label(text=f"Status: {res.get('status', 'pending')}"))

            cancel_btn = Button(text="Cancel", size_hint_y=None, height=40)
            cancel_btn.res_id = str(res["_id"])
            cancel_btn.bind(on_release=self.cancel_reservation)
            box.add_widget(cancel_btn)

            container.add_widget(box)

    def cancel_reservation(self, btn):
        print(f"Cancelling reservation with ID: {btn.res_id}")
        db.cancel_reservation(btn.res_id)
        self.load_reservations()

    def go_back(self):
        self.manager.current = "dashboard"


class GuestApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(WelcomeScreen(name='welcome'))
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(RegisterScreen(name='register'))
        sm.add_widget(DashboardScreen(name='dashboard'))
        sm.add_widget(ReservationScreen(name='reservation'))
        sm.add_widget(MyReservationsScreen(name='my_reservations'))
        return sm


if __name__ == "__main__":
    GuestApp().run()
