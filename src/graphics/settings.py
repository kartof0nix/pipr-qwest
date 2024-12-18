
from __future__ import annotations
from typing import List, Any
import urwid
from collections.abc import Iterable
from common.config import Setting, registered_settings
from graphics.common import Clickable


    

class SelectBox(urwid.Text):
    def __init__(self, select_list, current : str = None):
        self.select = select_list
        self.iter = 0
        if(current != None):
            self.iter = select_list.index(current)
        super().__init__(self.render_text())
    
    def render_text(self):
        return str(self.select[self.iter]) 

    def get_value(self):
        return self.select[self.iter]
    
    def decrement(self, source = None):
        self.iter = (self.iter - 1) % len(self.select)
        self.set_text(self.render_text())

    def increment(self, source = None):
            self.iter = (self.iter + 1) % len(self.select)
            self.set_text(self.render_text())
        
    def keypress(self, size: tuple[()] | tuple[int] | tuple[int, int], key: str) -> str | None:
        if(key == "left"):
            self.decrement()
            return
        if(key == "right"):
            self.increment()
            return
        return key
    
    def selectable(self):
        return True

class ValueBox(urwid.Text):
    def __init__(self, min_val : int | float, max_val : int | float, current : int | float):
        self.min_val = min_val
        self.max_val = max_val
        self.current = current
        self.type = type(current)
        self.step = self.type((self.max_val - self.min_val) * 0.01)
        if(self.type == int): self.step = max(1, self.step)
        
        super().__init__(self.render_text())
    
    def render_text(self):
        return str(self.current)
    
    def decrement(self, source = None):
        self.current = max(self.current - self.step, self.min_val)
        if(self.type == float): self.current = round(self.current, 4)
        self.set_text(self.render_text())
        
    def increment(self, source = None):
        self.current = min(self.current + self.step, self.max_val)
        if(self.type == float): self.current = round(self.current, 4)
        self.set_text(self.render_text())
        
    def keypress(self, size: tuple[()] | tuple[int] | tuple[int, int], key: str) -> str | None:
        if(key == "left"):
            self.decrement()
            return
        if(key == "right"):
            self.increment()
            return
        return key
    
    def get_value(self):
        return self.current
    def selectable(self):
        return True


class SettingsItem(urwid.AttrMap):
    def __init__(self, item : str, widget : urwid.Widget, title : str = None):
        self.item = item
        if(title == None): title = item.capitalize().replace('_', ' ') + ": " 
        self.left = urwid.Text(title)
        self.right = widget
        dec = Clickable("<", self.right.decrement)
        inc = Clickable(">", self.right.increment)
        # urwid.connect_signal(dec, "click", self.right.decrement())
        # urwid.connect_signal(inc, "click", self.right.increment())
        super().__init__(urwid.Columns([('pack', self.left), ('pack', dec), ('pack', self.right), ('pack', inc),], focus_column=1), None, focus_map="reversed")

class SettingsView(urwid.Pile):
    def apply(self, button : urwid.Button):
        for it in self.body:
            self.pages[self.current].set_value(it.item, it.right.get_value())
        self.pages[self.current].save_to_file()
    def exit(self, button : urwid.Button):
        raise urwid.ExitMainLoop()
    
    def subpage(self, s : Setting):
        header = [urwid.Text(s.name), urwid.Divider()]
        self.body = []
        for item in s.config:
            if(s.constrains[item]['value_type'] == "selectable"):
                self.body.append(SettingsItem(item, SelectBox(s.constrains[item]['selectable'], s.config[item])))
            if(s.constrains[item]['value_type'] == "bound"):
                self.body.append(SettingsItem(item, ValueBox(s.constrains[item]['min_val'], s.constrains[item]['max_val'], s.config[item])))
        apply_bt = urwid.AttrMap( urwid.Button("Apply", self.apply), "button", focus_map="reversed_button" )
        exit_bt = urwid.AttrMap( urwid.Button("Close", self.exit), "button", focus_map="reversed_button" )
        footer = [urwid.Divider(), urwid.Columns([("pack", apply_bt), ("pack", exit_bt)], dividechars=2)]
        # body.append(urwid.Button())
        return urwid.ListBox(urwid.SimpleFocusListWalker(header + self.body + footer))
    def __init__(self, settings : List[Setting]):
        self.pages = settings
        self.current = 0
        super().__init__([self.subpage(self.pages[self.current])])
    # def __init__(self, widget_list, focus_item = None):
        # super().__init__(widget_list, focus_item)




def render():
    ses = SettingsView(registered_settings)

    main = urwid.Padding(ses, left=2, right=2)

    top = urwid.Overlay(
        main,
        urwid.SolidFill("\N{MEDIUM SHADE}"),
        align=urwid.CENTER,
        width=(urwid.RELATIVE, 60),
        valign=urwid.MIDDLE,
        height=(urwid.RELATIVE, 60),
        min_width=20,
        min_height=9,
    )
    palette = [("reversed", "standout", ""), ("button", "light cyan", ""), ("reversed_button", "black", "light cyan")]
    
    urwid.MainLoop(top, palette=palette).run()