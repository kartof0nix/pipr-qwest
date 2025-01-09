from typing import Literal, Tuple
import urwid
import asyncio

'''Main view class - the manager for widgets, views and general configuration'''

import logging
logger = logging.getLogger(__name__)

# async def test():

palette = [("reversed", "standout", ""),
           ("button", "light cyan", ""),
           ("reversed_button", "black", "light cyan"),
           ("button2", "yellow", ""),
           ("reversed_button2", "black", "dark red"),
           ("banner", "", "", "", "#ffa", "#60d"),
           ("bold", "white,bold", ""),
           ("italics", "white,italics", ""),
           ("streak", "", "", "", "g50", "#60a"),
           ("inside", "", "", "", "g38", "#808"),
           ("outside", "", "dark gray", "", "g27", "#333"),
           ("bg", "", "", "", "g7", "#033"),
           ("cyan", "dark cyan", ""),
           ("magenta","dark magenta", ""),
           ("default", "", ""),
           ("yellow", "yellow", ""),
           ("green", "dark green", ""),

           ("pyellow", "yellow,bold", ""),
           ("pwhite", "white,bold", ""),
           ("hwhite", "white,bold", ""),
           ("hred", "dark red,bold", ""),
           ("hblue", "dark blue,bold", ""),
           ("hgreen", "dark green,bold", ""),
           ("hbrown", "black", "brown"),
           ]
class myOverlay(urwid.Overlay):
    def keypress(self, size, key):
        key = super().keypress(size, key)
        if(key != None):
            return self.bottom_w.keypress(size, key)

class blockLineBock(urwid.LineBox):
    def keypress(self, size, key):
        key = super().keypress(size, key)
        if(key != None and not key in ['up', 'down', 'left', 'right', 'i']):
            return key
    
class MainView(urwid.WidgetPlaceholder):
    def is_overlayed(self):
        return type(self.main_placeholder.original_widget) == myOverlay
    def get_top(self):
        return self.main_placeholder.original_widget.top_w

    def pop_top(self):
        logger.debug("Popping top overlay. Current top : %s",
                     repr(self.main_placeholder.original_widget))
        if not(self.is_overlayed()):
            logger.error(
                "Attempted to pop overlay whilst no overlay is active.")
            return
        self.main_placeholder.original_widget = self.main_placeholder.original_widget.bottom_w
        loop.draw_screen()
    
    def push_top(self,
                widget: urwid.Widget,
                width: Literal["pack"] | int | tuple[Literal["relative"], int] | None,
                height: int | tuple[Literal["relative"], int] | None,
                halign: Literal["left", "center", "right"],
                valign=Literal['top', 'middle', 'bottom']
    ):
        placeholder = self.main_placeholder
        logger.debug("Pushing %s. Current top placeholder : %s",
                     repr(widget), repr(self.main_placeholder))
        ov = myOverlay(
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
        # if key in ("q", "Q"):
        #     aloop.create_task(self.exit())
        super().keypress(size, key)
    def stop(self):
        raise urwid.ExitMainLoop()
    def selectable(self):
        return True


def add_frame(
    widget : urwid.Widget,
    width: Literal["pack"] | int | tuple[Literal["relative"], int] | None,
    height: int | tuple[Literal["relative"], int] | None,
    side : Literal['left', 'top', 'right', 'bottom'] | Tuple[Literal['left', 'center', 'bottom'], Literal['top', 'middle', 'bottom']],
    title:str="",
    block_move:bool=False
):
    if(type(side) == tuple):
        (halign, valign) = side
    else:
        halign = {'left':'left', 'top':'center', 'right':'right', 'bottom':'center'}[side]
        valign = {'left':'middle', 'top':'top', 'right':'middle', 'bottom':'bottom'}[side]
    if not block_move:
        line_box = urwid.LineBox(urwid.Filler(widget, valign="top"), title)
    else:
        line_box = blockLineBock(urwid.Filler(widget, valign="top"), title)
        
    # filler = urwid.Filler(line_box)
    
    view.push_top(line_box, width=width+2 if type(width)==int else width, height=height+2 if type(height)==int else height, halign=halign, valign=valign)

def get_frame():
    return view.get_top().original_widget.original_widget.original_widget.original_widget

def rem_frame():
    view.pop_top()
    

    

view = MainView()
'''Urwid main loop. Use to re-draw screen after update'''
def render(callback, exitFunction):
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
    view.exit = exitFunction
    loop.screen.set_terminal_properties(colors=2**24)
    # self.draw_main()
    aloop.create_task(callback())
    loop.run()
    

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
