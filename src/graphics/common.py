import urwid

class CustomButton(urwid.Button):
    def __init__(self, label, on_press=None, user_data=None, prefix='', suffix=''):
        super().__init__("")
        self.prefix = prefix
        self.suffix = suffix

        # Create a custom layout for the button
        self._label_widget = urwid.Text("")
        self.set_label(label)

        self._w = urwid.Padding(
            urwid.Columns([
                (len(self.prefix), urwid.Text(self.prefix)),
                self._label_widget,
                (len(self.suffix), urwid.Text(self.suffix)),
            ]),
            left=1, right=1
        )
        if on_press:
            urwid.connect_signal(self, 'click', on_press, user_data)

    def set_label(self, label):
        """Set the button's label."""
        self._label_widget.set_text(label)

def buttonAttr(button:urwid.Button):
    return urwid.AttrMap( button, "button", focus_map="reversed_button" )

def niceFiller(widget : urwid.Widget):
    return urwid.AttrMap(urwid.Filler(urwid.Padding(urwid.AttrMap(widget, "bg"), align='center', width=('relative', 90) )), "outside")