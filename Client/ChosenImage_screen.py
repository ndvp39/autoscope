from kivy.uix.screenmanager import Screen
from kivy.core.image import Image as CoreImage
from config import SERVER_URL
import requests


class ChosenImageScreen(Screen):
    def __init__(self, **kwargs):
        super(ChosenImageScreen, self).__init__(**kwargs)
        self.image_path = None
        self.image = None
        self.user_id = None
        self.chosen_current_image = None

    def update_data(self, image_path, user_id):
        self.image_path = image_path
        self.user_id = user_id
        self.image = None
        self.display_image()

    def display_image(self):
        if self.image_path:
            try:
                img = CoreImage(self.image_path)
                self.ids.image_display.texture = img.texture
                self.chosen_current_image = img
                print(f"Image loaded: {self.image_path}")
            except Exception as e:
                print(f"Error loading image: {e}")
                self.ids.image_display.texture = None

    def go_back(self):
        self.manager.current = 'earCheck'

    def analyze_image(self):
        if not self.image_path:
            print("No image selected.")
            return

        try:
            url = f"{SERVER_URL}/api/analyze_image"
            with open(self.image_path, 'rb') as image_file:
                files = {'image': image_file}
                data = {'user_id': str(self.user_id)}
                response = requests.post(url, files=files, data=data)
                response.raise_for_status()
                response_data = response.json()

                confidence = response_data.get("confidence")
                predicted_class = response_data.get("predicted_class")

                results_screen = self.manager.get_screen('result')
                results_screen.update_data(self.chosen_current_image, f"{predicted_class} {confidence}", self.user_id)
                self.manager.current = 'result'
        except requests.exceptions.RequestException as e:
            print(f"Error during analysis request: {e}")

