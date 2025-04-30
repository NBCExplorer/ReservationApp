from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder

# Loads KV layout
Builder.load_file('ui.kv')

# Welcome Screen
class WelcomeScreen(Screen):
    pass

# Login Screen (without DB)
class LoginScreen(Screen):
    def login_guest(self):
        # Simple email and password check (hardcoded)
        email = self.ids.email_input.text
        password = self.ids.password_input.text
        
        if email == "guest@example.com" and password == "password123":
            self.manager.current = "guest_home"
        else:
            self.ids.login_status.text = "Login failed. Try again."

# Register Screen (without DB)
class RegisterScreen(Screen):
    def register_guest(self):
        first_name = self.ids.reg_firstname_input.text
        last_name = self.ids.reg_lastname_input.text
        full_name = f"{first_name} {last_name}"
        email = self.ids.reg_email_input.text
        password = self.ids.reg_password_input.text
        
        if email and password:  # Basic check if fields are filled
            self.manager.current = "login"
        else:
            self.ids.register_status.text = "Please fill in all fields."

# Guest Home Screen
class GuestHomeScreen(Screen):
    def logout_guest(self):
        self.manager.current = "welcome"

# Main App Class
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
