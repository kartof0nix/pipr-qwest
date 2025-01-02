import urwid

# Create a filler widget to put inside the LineBox
content = urwid.Text("Content")

# Use BoxAdapter to fix the height of the content to 2 (total height = content + 2 frame rows)
fixed_height_content = urwid.BoxAdapter(urwid.Filler(content, valign="top"), height=2)

# Wrap the content with a LineBox
line_box = urwid.LineBox(fixed_height_content)

# Create the main loop
loop = urwid.MainLoop(urwid.Filler(line_box, valign="top"))
loop.run()
