'''
Call the package directly to run it.
'''
from pathlib import Path
import logging
from typing import List

logger = logging.getLogger(__name__)
logging.basicConfig(filename='qwest.log',
                        level=logging.INFO, filemode="w")

import urwid
import asyncio
from src.graphics import tui_main
from src.level import LevelManager
from src.globals import player
from src.common import event_queue
from src.graphics.settings import launchSettings
from src.graphics.common import buttonAttr, buttonAttr2, niceFiller
# a = fabricCanvas([["a", "b"], ["c", "d"]], [["", ""], ["", ""]])
# for c in a.content():
#     print(c)
# print(a.content())



class editWindow(urwid.Edit):
    def __init__(self, caption = "", edit_text = "", multiline = False):
        self.complete = asyncio.Event()
        super().__init__(caption, edit_text, multiline)
    def keypress(self, size, key):
        if(key=='enter'):
            self.complete.set()
        else:
            return super().keypress(size, key)
    async def get(self):
        await self.complete.wait()
        return self.get_edit_text()

class SelectSaveView(urwid.Pile):
    async def _select(self, butt:urwid.Button):
        self.res = butt.get_label()
        if(butt.get_label() == "New save"):
            label = "Choose save name"
            w = editWindow(label+"\n")
            tui_main.add_frame(w, len(label), height=3, side='bottom')
            self.res = await w.get()
            tui_main.rem_frame()
        self.selected.set()
        pass
    def select(self, butt:urwid.Button):
        asyncio.create_task(self._select(butt))
    def __init__(self):
        self.res = None
        self.selected = asyncio.Event()
        saves = player.listSaves()
        widget_list = [buttonAttr(urwid.Button(i, self.select)) for i in saves]
        widget_list = [urwid.Text(("bold", "Select save:")), urwid.Divider()] + widget_list
        widget_list.append(urwid.Divider())
        widget_list.append(buttonAttr2(urwid.Button("New save", self.select)))
        widget_list.append(urwid.Divider())
        widget_list.append(urwid.Text(("italics", "Press d to delete save")))
        super().__init__(widget_list)
        
    def keypress(self, size, key):
        if(key=='d'):
            logger.info("remove save %s", self.focus.base_widget.get_label())
            player.removeSave(self.focus.base_widget.get_label())
            self.selected.set()
        return super().keypress(size, key)
    async def choice(self):
        await self.selected.wait()
        return self.res
    
async def launchSelect():
    res = None
    lastBottom = tui_main.view.bottom
    while(res == None):
        sel = SelectSaveView()
        tui_main.view.bottom = niceFiller(sel)
        res = await sel.choice()
    tui_main.view.bottom = lastBottom
    asyncio.create_task(main.startGame(res))


            
class MainView(urwid.Pile):
    def playButton(self, butt : urwid.Button):
        asyncio.create_task(launchSelect())
    def exitButton(self, butt : urwid.Button):
        raise urwid.ExitMainLoop()
    def settingsButton(self, butt : urwid.Button):
        asyncio.create_task(launchSettings())
        
    def __init__(self):
        menu = urwid.Pile([
            buttonAttr(urwid.Button("Play!", self.playButton )),
            buttonAttr(urwid.Button("Settings", self.settingsButton )),
            urwid.Divider(top=4),
            buttonAttr(urwid.Button("Exit", self.exitButton )),
            
        ])
        widgets = [
            urwid.Padding(urwid.BigText(('banner', "Pipr Qwest"), urwid.HalfBlock5x4Font()),width='clip', align='center'),
            urwid.Divider(top=3),
            urwid.Padding(menu, align='center', width=('relative', 90))
        ]
        super().__init__(widgets)

class Main:
    
    async def exit(self):
        player.player.save_to_file()
        tui_main.view.stop()
    

    async def startGame(self, save:str):
        player.loadSave(save)
        lvl = LevelManager.callLevel(player.player['currentLevel'])
        logger.info(f"Game loaded")
    # async 
    #     await asyncio.sleep(10)
    #     logger.info(f"Del gameq")
    #     player.player['currentLevel'] = 'asriel_passage.json'
    #     LevelManager.delLevel()
        # del lvl
    
# a = input("Select level")
main = Main()
mainView = MainView()

async def loadMainView():
    tui_main.aloop.create_task(event_queue.loop())
    tui_main.view.bottom=niceFiller(mainView)
tui_main.render(loadMainView, main.exit)

