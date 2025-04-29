from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder

# Define the Screens
class WelcomeScreen(Screen):
    pass

class LoginScreen(Screen):
    def login_guest(self):
        # For now, just navigate to guest home
        self.manager.current = "guest_home"

class RegisterScreen(Screen):
    def register_guest(self):
        # For now, just navigate back to login after "registration"
        self.manager.current = "login"

class GuestHomeScreen(Screen):
    def logout_guest(self):
        self.manager.current = "welcome"

class GuestApp(App):
    def build(self):
        # Load the separate KV file automatically
        Builder.load_file('ui.kv')
        sm = ScreenManager()
        sm.add_widget(WelcomeScreen(name='welcome'))
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(RegisterScreen(name='register'))
        sm.add_widget(GuestHomeScreen(name='guest_home'))
        return sm

if __name__ == "__main__":
    GuestApp().run()
