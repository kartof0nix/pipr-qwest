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

palette = [("reversed", "standout", ""),
           ("button", "light cyan", ""),
           ("reversed_button", "black", "light cyan"),
           ("banner", "", "", "", "#ffa", "#60d"),
           ("streak", "", "", "", "g50", "#60a"),
           ("inside", "", "", "", "g38", "#808"),
           ("outside", "", "", "", "g27", "#a06"),
           ("bg", "", "", "", "g7", "#d06"),
           ("cyan", "dark cyan", ""),
           ("magenta","dark magenta", ""),
           ("default", "", ""),
           ("pyellow", "yellow,bold", ""),
           ("pwhite", "white,bold", ""),
           ("hwhite", "white,bold", ""),
           ("hred", "dark red,bold", ""),
           ("hblue", "", "dark blue"),
           ("hbrown", "", "brown")
           ]


class MainView(urwid.WidgetPlaceholder):

    def get_top(self):
        return self.main_placeholder.original_widget.top_w

    def pop_top(self):
        logger.debug("Popping top overlay. Current top : %s",
                     repr(self.main_placeholder.original_widget))
        if (type(self.main_placeholder.original_widget) != urwid.Overlay):
            logger.error(
                "Attempted to pop overlay whilst no overlay is active.")
            return
        self.main_placeholder.original_widget = self.main_placeholder.original_widget.bottom_w
        loop.draw_screen()
    def push_top(self, widget: urwid.Widget, width: int, height: int, halign: Literal["left", "center", "right"], valign=Literal['top', 'middle', 'bottom']):
        placeholder = self.main_placeholder
        logger.debug("Pushing %s. Current top placeholder : %s",
                     repr(widget), repr(self.main_placeholder))
        ov = urwid.Overlay(
            bottom_w=self.main_placeholder.original_widget,
            top_w=widget,
            align=halign,
            valign=valign,
            width=width,
            height=height,
            left=2,
            right=2,
            top=1,
            bottom=1
        )
        logger.debug("New back placeholder : %s", repr(ov))
        self.main_placeholder.original_widget = ov
        loop.draw_screen()
        return
        if (side == "left"):
            pass
        if (side == "right"):
            ov = urwid.Overlay(
                placeholder.original_widget,
                widget,
                'right',
                width,
                valign="middle",
                right=2
            )
        if (side == "top"):
            ov = urwid.Overlay(
                placeholder.original_widget,
                widget,
                'top',
                width,
                align="middle",
                top=2
            )
        if (side == "bottom"):
            ov = urwid.Overlay(
                placeholder.original_widget,
                widget,
                'bottom',
                width,
                align="middle",
                bottom=2
            )

    @property
    def bottom(self) -> urwid.Widget:
        return self.bottom_placeholder.original_widget

    @bottom.setter
    def bottom(self, widget: urwid.Widget):
        self.bottom_placeholder.original_widget = widget

    def __init__(self):
        self.bottom_placeholder = urwid.WidgetPlaceholder(
            urwid.SolidFill(u'+'))
        self.main_placeholder =  urwid.WidgetPlaceholder(self.bottom_placeholder)
        super(MainView, self).__init__(self.main_placeholder)

        # self.box_level = 0
        # self.open_box(box)

        # Run the application with the placeholder
    def keypress(self, size, key):
        if key in ("q", "Q"):
            raise urwid.ExitMainLoop()
        super().keypress(size, key)

    def selectable(self):
        return True


def add_frame(widget : urwid.Widget, width:int, height:int, side : Literal['left', 'top', 'right', 'bottom'], title=""):
    halign = {'left':'left', 'top':'center', 'right':'right', 'bottom':'center'}[side]
    valign = {'left':'middle', 'top':'top', 'right':'middle', 'bottom':'bottom'}[side]
    fixed_height_content = urwid.BoxAdapter(urwid.Filler(widget, valign="top"), height=height)
    line_box_widget = urwid.Filler(urwid.LineBox(fixed_height_content, title))
    logger.info(line_box_widget.sizing())
    view.push_top(line_box_widget, width=width+2, height=height+2, halign=halign, valign=valign)

def get_frame():
    return view.get_top().original_widget.original_widget.original_widget.original_widget

def rem_frame():
    view.pop_top()
    

    

view = MainView()
'''Urwid main loop. Use to re-draw screen after update'''
def render(callback):
    '''
    Render the main view. Since urwid needs to manage asyncio, use callback asyc function to continue execution of main program.
    '''
    urwid.set_encoding("UTF-8")
    global loop
    global aloop
    null_widget = urwid.Text(("banner", "Null"), align="center")
    null_filler = urwid.Filler(null_widget, valign="middle")
    null_attr = urwid.AttrMap(null_filler, "bg")
    main_placeholder = urwid.WidgetPlaceholder(null_attr)

    aloop = asyncio.new_event_loop()
    ev_loop = urwid.AsyncioEventLoop(loop=aloop)

    loop = urwid.MainLoop(view, palette=palette, event_loop=ev_loop)
    loop.screen.set_terminal_properties(colors=256)
    # self.draw_main()
    aloop.create_task(callback())
    loop.run()
    

'''Main asyncio event loop'''
# global aloop
# aloop = None
# global loop
# loop = None

# --- Test module --- 

async def test_view():
    logger.info("Awaiting")
    await asyncio.sleep(2)
    logger.info("Creating widget 1")
    add_frame(urwid.Text("This is some text inside a fixed-size LineBox."), 6, 10, 'left', 'tet')
    logger.info("Created widget 1")
    await asyncio.sleep(4)
    add_frame(urwid.Text("You're bad at programming"), 40, 2, 'bottom', "You like kissing boys, don't you?")
    logger.info("Created widget 2")
    await asyncio.sleep(4)
    logger.info("Modified widget 2")
    get_frame().set_text("I changed my mind")
    loop.draw_screen()
    await asyncio.sleep(4)
    logger.info("Modified bg")
    view.bottom = urwid.SolidFill(u'#')
    loop.draw_screen()
    await asyncio.sleep(2)
    logger.info("Removed widget 2")
    view.pop_top()
    
    

if __name__ == "__main__":
    logging.basicConfig(filename='qwest.log',
                        level=logging.DEBUG, filemode="w")
    logger.info(f"Starting test module {__package__}")
    # asyncio.create_task(create_panes())
    render(test_view)
