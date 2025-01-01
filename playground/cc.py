import urwid
import asyncio

class mainView():
    # Base widget
    base_text = urwid.Text("This is the main application screen.", align="center")
    base_widget = urwid.Filler(base_text, valign="middle")

    # Create a placeholder for dynamic updates
    placeholder = urwid.WidgetPlaceholder(base_widget)

    # Function to show the dialog
    def show_dialog(self):
        dialog_text = urwid.Text("This is a dialog box.", align="center")
        dialog_buttons = urwid.Columns(
            [
                urwid.Button("OK", on_press=lambda button: exit_app()),
                urwid.Button("Cancel", on_press=lambda button: hide_dialog()),
            ],
            dividechars=2,
        )
        dialog_content = urwid.Pile([dialog_text, urwid.Divider(), dialog_buttons])
        dialog_box = urwid.LineBox(dialog_content, title="Dialog")
        dialog_overlay = urwid.Overlay(
            urwid.Filler(dialog_box, valign="middle", height=10),
            self.base_widget,
            align="center",
            width=40,
            valign="middle",
            height=10,
        )
        self.placeholder.original_widget = dialog_overlay
        # Schedule the dialog to be hidden after 5 seconds using asyncio
        # asyncio.create_task(hide_overlay_after(5))

    # Function to hide the dialog
    def hide_dialog(self):
        self.placeholder.original_widget = self.base_widget

    # Async function to hide the overlay after a delay
    async def hide_overlay_after(self, seconds):
        await asyncio.sleep(seconds)
        self.hide_dialog()  # Schedule UI updates safely
        self.loop.draw_screen()

    # Handle user input (for quitting)
    def handle_input(self, key):
        if key in ("q", "Q"):
            raise urwid.ExitMainLoop()

    # Start urwid's main loop and integrate with asyncio
    urwid_loop = urwid.MainLoop(placeholder, unhandled_input=handle_input)


    async def run(self):
        self.aloop = asyncio.get_event_loop()
        ev_loop = urwid.AsyncioEventLoop(loop=self.aloop)
        self.loop = urwid.MainLoop(self.placeholder, unhandled_input=self.handle_input, event_loop=ev_loop)
        self.aloop.create_task(self.hide_overlay_after(5))
        self.show_dialog()
        self.loop.run()

    # asyncio.run(combined_run())  # Start asyncio's event loop

def exit_app():
    raise urwid.ExitMainLoop()

if __name__ == "__main__":
    v = mainView()
    asyncio.run(v.run())
