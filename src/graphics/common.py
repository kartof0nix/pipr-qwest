import urwid
import urwid.text_layout
import asyncio

from src.graphics import tui_main


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


class notificationWidget(urwid.Pile):
    def confirm(self, button: urwid.Button = None):
        self.confirmed.set()
        if self.callback is not None:
            self.callback()

    def __init__(self, text, callback=None):
        self.callback = callback
        self.confirmed = asyncio.Event()
        widgets = [
            urwid.Text(('cyan', text)),
            urwid.Filler(buttonAttr(urwid.Button("Ok", self.confirm)))
        ]
        super().__init__(widgets)


def notify(text) -> notificationWidget:
    wgt = notificationWidget(text, tui_main.rem_frame)
    tui_main.add_frame(wgt, len(text) + 10, 2, ('center', 'middle'))
    return wgt


def buttonAttr(button: urwid.Button):
    return urwid.AttrMap(button, "button", focus_map="reversed_button")


def buttonAttr2(button: urwid.Button):
    return urwid.AttrMap(button, "button2", focus_map="reversed_button2")


def niceFiller(widget: urwid.Widget):
    return urwid.AttrMap(urwid.Filler(urwid.Padding(urwid.AttrMap(widget, "bg"), align='center', width=('relative', 90))), "outside")
