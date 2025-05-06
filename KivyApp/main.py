from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from db_layer import Database  # <- Import the DB handler

db = Database()  # <- Create a single instance

Builder.load_file('ui.kv')

class WelcomeScreen(Screen):
    pass

class LoginScreen(Screen):
    def login_guest(self):
        email = self.ids.email_input.text
        password = self.ids.password_input.text
        if db.validate_guest_login(email, password):
            self.manager.current = "guest_home"
        else:
            self.ids.login_status.text = "Login failed. Try again."

    def on_pre_leave(self):  # Clear status when leaving
        self.ids.login_status.text = ""

class RegisterScreen(Screen):
    def register_guest(self):
        first = self.ids.reg_firstname_input.text
        last = self.ids.reg_lastname_input.text
        email = self.ids.reg_email_input.text
        password = self.ids.reg_password_input.text

        if first and last and email and password:
            if db.register_guest(first, last, email, password):
                self.manager.current = "login"
            else:
                self.ids.register_status.text = "Email already exists."
        else:
            self.ids.register_status.text = "Please fill in all fields."

    def on_pre_leave(self):  # Clear status when leaving
        self.ids.register_status.text = ""

class GuestHomeScreen(Screen):
    def logout_guest(self):
        self.manager.current = "welcome"

class GuestApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(WelcomeScreen(name='welcome'))
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(RegisterScreen(name='register'))
        sm.add_widget(GuestHomeScreen(name='guest_home'))
        return sm

if __name__ == "__main__":
    GuestApp().run()
