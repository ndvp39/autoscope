from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from main_screen import MainScreen


class AutoScopeApp(App):
    def build(self):
        # Create ScreenManager and add screens
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        # sm.add_widget(AnalysisScreen(name='analysis'))
        # sm.add_widget(ResultScreen(name='result'))
        return sm

if __name__ == '__main__':
    AutoScopeApp().run()