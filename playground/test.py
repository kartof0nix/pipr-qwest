from textual.app import App
from textual.widgets import Button, Static

class OverlayApp(App):
    def compose(self):
        yield Static("This is the background", id="background")
        yield Static("Overlay widget", id="overlay", style="bold white on black")

    def on_mount(self):
        self.query_one("#overlay").styles.margin = (10, 10)  # Position overlay

OverlayApp().run()