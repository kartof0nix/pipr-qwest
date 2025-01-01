from __future__ import annotations

import urwid



def exit_on_q(key):

    if key in {"q", "Q"}:

        raise urwid.ExitMainLoop()


palette = [

    ("banner", "", "", "", "#80f", "#60d"),

    ("streak", "", "", "", "#80c", "#60a"),

    ("inside", "", "", "", "#808", "#808"),

    ("outside", "", "", "", "#c08", "#a06"),

    ("bg", "", "", "", "#f08", "#d06"),

]

palette = [

    ("banner", "", "", "", "#ffa", "#60d"),

    ("streak", "", "", "", "#000", "#60a"),

    ("inside", "", "", "", "#000", "#808"),

    ("outside", "", "", "", "#000", "#a06"),

    ("bg", "", "", "", "#000", "#d06"),

]


placeholder = urwid.SolidFill()

loop = urwid.MainLoop(placeholder, palette, unhandled_input=exit_on_q)

loop.screen.set_terminal_properties(colors=88)

loop.widget = urwid.AttrMap(placeholder, "bg")

loop.widget.original_widget = urwid.Filler(urwid.Pile([]))


div = urwid.Divider()

outside = urwid.AttrMap(div, "outside")

inside = urwid.AttrMap(div, "inside")

txt = urwid.Text(("banner", " Hello World "), align="center")

streak = urwid.AttrMap(txt, "streak")

pile = loop.widget.base_widget  # .base_widget skips the decorations

for item in (outside, inside, streak, inside, outside):

    pile.contents.append((item, pile.options()))


loop.run()
loop.run()