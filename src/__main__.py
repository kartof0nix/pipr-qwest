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
from src.logic.player import PlayerClass
from src.common import event_queue
from src.graphics.settings import SettingsView, registered_settings
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
        saves = main.listSaves()
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
            main.removeSave(self.focus.base_widget.get_label())
            self.selected.set()
        return super().keypress(size, key)
    async def choice(self):
        await self.selected.wait()
        return self.res
    
class MainView(urwid.Pile):
    async def launchSelect(self):
        res = None
        while(res == None):
            sel = SelectSaveView()
            tui_main.view.bottom = niceFiller(sel)
            res = await sel.choice()
        asyncio.create_task(main.startGame(res))
    
    def playButton(self, butt : urwid.Button):
        asyncio.create_task(self.launchSelect())
    
    def __init__(self):
        menu = urwid.Pile([
            buttonAttr(urwid.Button("Play!", self.playButton ))
        ])
        widgets = [
            urwid.Padding(urwid.BigText(('banner', "Pipr Qwest"), urwid.HalfBlock5x4Font()),width='clip', align='center'),
            urwid.Divider(top=3),
            urwid.Padding(menu, align='center', width=('relative', 90))
        ]
        super().__init__(widgets)

class Main:
    
    async def exit(self):
        self.player.save_to_file()
        tui_main.view.stop()
    
    def listSaves(self) -> List[str]:
        res = []
        try:
            # Create a Path object for the directory
            directory = Path(PlayerClass.CONFIG_PATH)
            for item in directory.iterdir():
                if item.is_file():
                    res.append(item.name.removesuffix(".json"))
        except Exception as e:
            logger.error("Listing saves failed : %s", e)
        return res
    def removeSave(self, save:str):
        save += ".json"
        file = Path(PlayerClass.CONFIG_PATH).joinpath(save)
        file.unlink()
        
    async def startGame(self, save:str):
        logger.info(f"Starting game %s", registered_settings)
        tui_main.view.bottom = SettingsView(registered_settings)
        self.player = PlayerClass(save + ".json")
        lvl = LevelManager.callLevel(self.player['currentLevel'], player=self.player)

        logger.info(f"Game loaded")
        tui_main.aloop.create_task(event_queue.loop())
    # async 
    #     await asyncio.sleep(10)
    #     logger.info(f"Del gameq")
    #     self.player['currentLevel'] = 'asriel_passage.json'
    #     LevelManager.delLevel()
        # del lvl
    
# a = input("Select level")
main = Main()
mainView = MainView()

async def loadMainView():
    tui_main.view.bottom=niceFiller(mainView)
tui_main.render(loadMainView, main.exit)

