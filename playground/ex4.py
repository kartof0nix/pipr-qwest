import urwid

class CustomButton(urwid.Button):
    def __init__(self, label, on_press=None, user_data=None, prefix='[', suffix=']'):
        super().__init__("")
        self.prefix = prefix
        self.suffix = suffix

        # Create a custom layout for the button
        self._label_widget = urwid.Text("")
        self.set_label(label)

        self._w = urwid.AttrMap(
            urwid.Padding(
                urwid.Columns([
                    (len(self.prefix), urwid.Text(self.prefix)),
                    self._label_widget,
                    (len(self.suffix), urwid.Text(self.suffix)),
                ]),
                left=1, right=1
            ),
            None,         # Normal state styling
            'button focus'  # Focused state styling
        )

        if on_press:
            urwid.connect_signal(self, 'click', on_press, user_data)

    def set_label(self, label):
        """Set the button's label."""
        self._label_widget.set_text(label)

# Callback for when the button is pressed
def on_button_pressed(button, user_data):
    print(f"Button '{user_data}' pressed!")

# Main function to display the button
def main():
    # Create the custom button
    button = CustomButton("Click Me!", on_press=on_button_pressed, user_data="Test", prefix="*", suffix="*")
    placeholder = urwid.Padding(button, left=2, right=2)

    # Add the button to a box and run the main loop
    loop = urwid.MainLoop(urwid.Filler(placeholder), unhandled_input=exit_on_q)
    loop.run()

def exit_on_q(key):
    if key in ('q', 'Q'):
        raise urwid.ExitMainLoop()

if __name__ == "__main__":
    main()
