from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from main_screen import MainScreen
from sign_up_screen import SignUpScreen


class UserLoginScreen(Screen):
    def __init__(self, **kwargs):
        super(UserLoginScreen, self).__init__(**kwargs)

        layout = FloatLayout()  # Use FloatLayout for positioning

        # Welcome text
        welcome_label = Label(
            text="Welcome to Autoscope",
            font_size=32,
            pos_hint={'center_x': 0.5, 'top': 0.95},
            size_hint=(None, None)
        )
        layout.add_widget(welcome_label)

        # Sign-in fields (email and password)
        self.email_input = TextInput(
            hint_text="Email",
            size_hint=(0.7, None),
            height=50,
            pos_hint={'center_x': 0.5, 'top': 0.7},
            multiline=False
        )
        layout.add_widget(self.email_input)

        self.password_input = TextInput(
            hint_text="Password",
            password=True,
            size_hint=(0.7, None),
            height=50,
            pos_hint={'center_x': 0.5, 'top': 0.6},
            multiline=False
        )
        layout.add_widget(self.password_input)

        # Sign-in and Create User buttons
        button_layout = BoxLayout(
            orientation='horizontal',
            size_hint=(0.7, None),
            height=50,
            pos_hint={'center_x': 0.5, 'top': 0.45},
            spacing=20
        )

        sign_in_button = Button(
            text="Sign In",
            size_hint=(0.5, None),
            height=50
        )
        sign_in_button.bind(on_release=self.sign_in_func)
        button_layout.add_widget(sign_in_button)

        create_user_button = Button(
            text="Create User",
            size_hint=(0.5, None),
            height=50
        )
        create_user_button.bind(on_release=self.sign_up_func)
        button_layout.add_widget(create_user_button)

        layout.add_widget(button_layout)

        self.add_widget(layout)

    
    def sign_in_func(self, instance):
        # Get the email and password entered by the user
        email = self.email_input.text
        password = self.password_input.text

        # Tester 
        #here call server functionality of user authentication
        if email == "test" and password == "test123":
            self.show_popup("Login Successful", "Welcome back!", self.open_main_screen)
        else:
            self.show_popup("Login Failed", "Invalid email or password")

    def sign_up_func(self, instance):
        signup_screen = SignUpScreen(name="SignUp")
        self.parent.add_widget(signup_screen)
        self.parent.current = "SignUp"
        
        
    def show_popup(self, title, message, callback=None):
        # Show a popup message to the user
        popup_layout = BoxLayout(orientation='vertical', padding=10)
        popup_label = Label(text=message)
        popup_button = Button(text='Close', size_hint=(1, 0.25))
        popup_layout.add_widget(popup_label)
        popup_layout.add_widget(popup_button)

        popup = Popup(title=title, content=popup_layout, size_hint=(0.7, 0.3))

        def on_close_popup(instance):
            popup.dismiss()
            if callback:
                callback()

        popup_button.bind(on_release=on_close_popup)
        popup.open()


    def open_main_screen(self):
        main_screen = MainScreen(name="main")
        self.parent.add_widget(main_screen)
        # Switch to the MainScreen
        self.parent.current = "main"  # This switches to the screen named "main"