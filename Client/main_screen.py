from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.graphics import Color, Rectangle
from menu_screen import MenuScreen
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from kivy.graphics.texture import Texture
from kivy.uix.image import Image as KivyImage
from kivy.core.image import Image as CoreImage
from kivy.uix.label import Label
from kivy.app import App
from menu_screen import MenuScreen
from rounded_button import RoundedButton


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

        self.menu_open = False  # Variable to track if the menu is open or closed

        layout = FloatLayout()  # Use FloatLayout for flexible positioning

        with layout.canvas.before:
            Color(0.2, 0.5, 0.8, 1)  # RGB for blue (0-1 range)
            self.rect = Rectangle(size=layout.size, pos=layout.pos)

        # Update the rectangle size when the layout size changes
        layout.bind(size=self._update_rect, pos=self._update_rect)

        # Create the image with size and allow_stretch
        otoscope_image = Image(
            source=r'Icons/otoscope.png',
            size_hint=(None, None),  # Disable size hint
            size=(150, 150),         # Set the desired size
            allow_stretch=True
        )
        # Center the image horizontally and position it slightly down from the top
        otoscope_image.pos_hint = {'center_x': 0.5, 'top': 0.65}
        layout.add_widget(otoscope_image)


        main_label = Label(
            text="Autoscope",
            font_size=32,
            pos_hint={'center_x': 0.5, 'top': 0.8},
            size_hint=(None, None)
        )
        layout.add_widget(main_label)

        sec_label = Label(
            text="Early detection of ear infections",
            font_size=24,
            pos_hint={'center_x': 0.5, 'top': 0.75},
            size_hint=(None, None)
        )
        layout.add_widget(sec_label)

        # Create the button layout below the image
        button_layout = BoxLayout(orientation='horizontal', size_hint=(None, None), pos_hint={'center_x': 0.35, 'center_y': 0.2}, spacing=50)   
        
        take_picture_button = RoundedButton(text='Take Picture', size_hint=(None, None), width=150, height=50)
        upload_picture_button = RoundedButton(text='Upload Picture', size_hint=(None, None), width=150, height=50)
        upload_picture_button.bind(on_release=self.open_file_explorer)

        button_layout.add_widget(take_picture_button)
        button_layout.add_widget(upload_picture_button)
        layout.add_widget(button_layout)

        # Create a button to open/close the MenuScreen in the top-left corner
        menu_button = RoundedButton(
            size_hint=(None, None),
            size=(75, 75),
            pos_hint={'x': 0, 'top': 1},
            background_normal=r'Icons/menu.png',  # Path to the button image
        )
        menu_button.bind(on_release=self.toggle_menu)
        layout.add_widget(menu_button)

        self.add_widget(layout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def toggle_menu(self, instance):
        # If the menu is open, remove it; if it's closed, add it
        if self.menu_open:
            self.remove_widget(self.menu)
        else:
            self.menu = MenuScreen(size_hint=(0.3, 1), pos_hint={'x': 0, 'y': 0}, manager=self.manager)
            self.add_widget(self.menu)
        self.menu_open = not self.menu_open  # Toggle the menu state

    def open_file_explorer(self, instance):
        # Create the file chooser
        filechooser = FileChooserIconView()

        # Create the select button
        select_button = RoundedButton(text='Select', size_hint=(1, None), height=50)  
        # Create the close button
        close_button = RoundedButton(text='Close', size_hint=(1, None), height=50)  
        # Layout for popup window with file chooser and buttons
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(filechooser)    
         # Horizontal layout for buttons
        button_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=50)
        button_layout.add_widget(select_button)
        button_layout.add_widget(close_button)
        
        layout.add_widget(button_layout)

        # Create the popup window
        popup = Popup(title='Select Image', content=layout, size_hint=(0.9, 0.9))

        # Function to handle selection of the image
        def select_image(instance):
            selected_image = filechooser.selection  # Get the selected image path
            if selected_image:
                image_path = selected_image[0]
                if self.is_image_file(image_path):

                    # Open the ChosenImageScreen with the selected image
                    app = App.get_running_app()

                    choseImage_screen = self.manager.get_screen('choseImage')
                    choseImage_screen.update_data(image_path=image_path, user_id=app.user_details.get("uid"))
                    self.manager.current = 'choseImage'

                    popup.dismiss()  # Close the popup once an image is selected
                else:
                    # Show error message if not a valid image
                    self.show_error_message(message='Invalid file type! Please select an image file.',text_color=(1, 0, 0, 1))
            else:
                popup.dismiss()  # Close the popup if no file is selected

        # Bind the select button to the image selection function
        select_button.bind(on_release=select_image)

        # Bind the close button to dismiss the popup
        close_button.bind(on_release=popup.dismiss)

        # Open the popup
        popup.open()


    def is_image_file(self, file_path):
        # Check if the file has a valid image extension
        valid_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff']
        return any(file_path.lower().endswith(ext) for ext in valid_extensions)
    
    def show_error_message(self, text_color=(1, 0, 0, 1), message=''):
        # Create a BoxLayout for the error message
        error_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=60, padding=10)
        
        # Create a label for the error message with dynamic text color
        error_label = Label(
            text=message,
            font_size=20,
            color=text_color
        )

        # Create a button to close the message
        close_button = RoundedButton(
            text='Close',
            size_hint=(None, None),
            width=100,
            height=50
        )
        close_button.bind(on_release=self.close_error_message)

        # Add the label and close button to the layout
        error_layout.add_widget(error_label)
        error_layout.add_widget(close_button)

        # Create a pop-up for the error message that will appear at the bottom
        self.error_popup = Popup(
            title='Error',
            content=error_layout,
            size_hint=(0.8, None),
            height=80,  # Set height to keep it at the bottom of the screen
            pos_hint={'x': 0.1, 'bottom': 0}  # Position the popup at the bottom
        )

        # Open the error popup
        self.error_popup.open()

    def close_error_message(self, instance):
        # Dismiss the error popup
        self.error_popup.dismiss()
