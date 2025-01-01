from typing import Literal
import urwid
import asyncio


import logging
logger = logging.getLogger(__name__)

text = """Initially, Pomni has a high-strung, timid, and tense demeanor. In the pilot episode, she is shown to be extremely anxious and troubled regarding her predicament, even succumbing to denial and exhibiting signs of delusion. When she finds the "exit", she experiences moderate signs of paranoia and seems to believe she is hallucinating. She's also on the clumsy side, as she tends to accidentally bump into things and people.

In her initial appearance, Pomni is shown to have a degree of both empathy and selfishness, as she goes back to check on Ragatha after the latter was attacked by an abstracted Kaufmo and promises Ragatha that she'd find Caine to fix her. However, Pomni's desire to escape the digital circus overrode this, as she entered the exit door upon finding it and left Ragatha behind. She later felt remorse for this action once Ragatha was fixed by Caine.

After having somewhat come to terms with her circumstances, Pomni adopts a more apathetic and cynical view, pointing out discrepancies in the Circus's scenarios and being detached from the adventures, not seeing the point in following along. She also seems to be more hot-tempered as she yells at the gang (specifically Jax) for their plans leaving her in mortal peril. Despite this, Pomni seems rather compassionate as she comforts and bonds with Gummigoo during his existential crisis, encouraging him by telling him he still has purpose and even inviting him to follow her back to the Circus. Overtime Pomni grew closer to the others after seeing how much they cared for each other during Kaufmo's funeral, and after receiving sound advice from Kinger (who temporarily regained his sanity), she thanked Ragatha for always being considerate to her and apologized for not showing appreciation until that moment.

Later in episode 4, she seems to have adapted more to being in the circus. She sees Gummigoo again and doesn't breakdown, she enters normal conversations with people like Jax, and shows concern for Gangle, asking if anyone could help her with her issues. She even offers to stay behind to close the restaurant when she sees that Gangle is sad. """

# async def test():
    
class mainView:
    palette = [("reversed", "standout", ""),
               ("button", "light cyan", ""), 
               ("reversed_button", "black", "light cyan"),
               ("banner", "", "", "", "#ffa", "#60d"),
               ("streak", "", "", "", "g50", "#60a"),
               ("inside", "", "", "", "g38", "#808"),
               ("outside", "", "", "", "g27", "#a06"),
               ("bg", "", "", "", "g7", "#d06")
    ]
    
    null_widget = urwid.Text("", align="center")
    main_placeholder = urwid.WidgetPlaceholder(null_widget)
    def back_placeholder(self):
        current_widget = self.main_placeholder
        while(type(current_widget.original_widget) == urwid.Overlay ):
            current_widget = current_widget.original_widget.bottom_w
        return current_widget
    def replace_back(self, widget : urwid.Widget):
        placeholder = self.back_placeholder()
        placeholder.original_widget = widget
    def pop_back(self):
        placeholder = self.back_placeholder()
        current_widget = self.main_placeholder
        try:
            while(type(current_widget.original_widget.bottom_w.original_widget) == urwid.WidgetPlaceholder ):
                current_widget = current_widget.original_widget.bottom_w
            current_widget.original_widget = current_widget.original_widget.top_w
        except Exception:
            logger.warning("Popping overlay failed")
    def append_back(self, widget:urwid.Widget, width : int, height : int, side : Literal["left", "top", "right", "bottom"]):
        placeholder = self.back_placeholder()
        logger.debug("Back placeholder : %s", repr(placeholder))
        ov = None
        ov = urwid.Overlay(
            top_w=widget,
            bottom_w=placeholder.original_widget,
            align='left',
            width=width,
            valign='middle',
            height=height,
            left=2,
            right=2,
            top=1,
            bottom=1
        )
        logger.debug("New back placeholder : %s", repr(ov))
        placeholder.original_widget = ov
        return
        if(side == "left"):
            pass
        if(side == "right"):
            ov = urwid.Overlay(
                placeholder.original_widget,
                widget,
                'right',
                width,
                valign="middle",
                right=2
            )
        if(side == "top"):
            ov = urwid.Overlay(
                placeholder.original_widget,
                widget,
                'top',
                width,
                align="middle",
                top=2
            )
        if(side == "bottom"):
            ov = urwid.Overlay(
                placeholder.original_widget,
                widget,
                'bottom',
                width,
                align="middle",
                bottom=2
            )
        
    
    def __init__(self):
        # Base widget
        null_widget = urwid.Text(("banner", "Null"), align="center")
        null_filler = urwid.Filler(null_widget, valign="middle")
        null_attr = urwid.AttrMap(null_filler, "bg")
        self.main_placeholder = urwid.WidgetPlaceholder(null_attr)
        

        # Run the application with the placeholder
    def run(self, callback):
        self.aloop = asyncio.new_event_loop()
        # self.aloop = asyncio.get_event_loop()
        # self.aloop.stop()
        ev_loop = urwid.AsyncioEventLoop(loop=self.aloop)
        self.loop = urwid.MainLoop(self.main_placeholder, palette=self.palette, unhandled_input=self.handle_input, event_loop=ev_loop)
        self.loop.screen.set_terminal_properties(colors=256)
        # self.draw_main()
        self.aloop.create_task(callback())
        self.loop.run()
        # self.loop.draw_screen()
        # asyncio.create_task()
        # self.aloop.create_task(self.hide_overlay_after(5))
        # self.show_dialog()

    def handle_input(self, key):
        if key in ("q", "Q"):
            raise urwid.ExitMainLoop()

        # Show the dialog on startup


view = mainView()

def exit_app():
    raise urwid.ExitMainLoop()

async def create_panes():
    logger.info("Awaiting")
    await asyncio.sleep(2)
    logger.info("Creating widget 1")
    text_widget = urwid.Text("This is some text inside a fixed-size LineBox.")

    # Create a Pile or another container for the Text widget if needed
    fixed_text_widget = urwid.Pile([text_widget])

    # Set a fixed size for the text widget using a Filler or directly via BoxAdapter (if needed)
    line_box_widget = urwid.LineBox(fixed_text_widget, title="Fixed LineBox")

    # Wrap the LineBox in a Filler to handle alignment and size
    view.append_back(urwid.Filler(line_box_widget, height=10), 10, 10, 'left')
    logger.info("Created widget 1")

    text_widget = urwid.Text("Test 2")

    # Create a Pile or another container for the Text widget if needed
    fixed_text_widget = urwid.Pile([text_widget])

    # Set a fixed size for the text widget using a Filler or directly via BoxAdapter (if needed)
    line_box_widget = urwid.LineBox(fixed_text_widget, title="Fixed LineBox")

    # Wrap the LineBox in a Filler to handle alignment and size
    view.append_back(urwid.Filler(line_box_widget, height=3), 10, 10, 'bottom')

    



if __name__ == "__main__":
    logging.basicConfig(filename='qwest.log', level=logging.DEBUG, filemode="w")
    logger.info("Starting [...]")
    # asyncio.create_task(create_panes())
    view.run(create_panes)
    # asyncio.create_task(view.run())
    # view.run()
    logger.info("Stopiing [...]")


        # show_dialog()
        
        # Function to show the dialog
        # def show_dialog():
        #     dialog_text = urwid.Text("This is a dialog box.", align="center")
        #     dialog_buttons = urwid.Columns(
        #         [
        #             urwid.Button("OK", on_press=lambda button: exit_app()),
        #             urwid.Button("Cancel", on_press=lambda button: hide_dialog()),
        #         ],
        #         dividechars=2,
        #     )
        #     dialog_content = urwid.Pile([dialog_text, urwid.Divider(), dialog_buttons])
        #     dialog_box = urwid.LineBox(dialog_content, title="Dialog")
        #     dialog_overlay = urwid.Overlay(
        #         urwid.Filler(dialog_box, valign="middle", height=10),
        #         base_widget,
        #         align="center",
        #         width=40,
        #         valign="middle",
        #         height=10,
        #     )
        #     placeholder.original_widget = dialog_overlay

        # Function to hide the dialog
        # def hide_dialog():
        #     placeholder.original_widget = base_widget

        # Handle user input (for navigation and quitting)