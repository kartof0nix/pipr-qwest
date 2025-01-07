import urwid
from src.logic.player import PlayerClass
from src.common import event_queue
class overlayWidget(urwid.Pile):
    def update(self):
        self.widgetList[0].set_text(["Health:", str(self.player['health'])])
    async def eventHandler(self, params=None):
        self._invalidate()
    def __init__(self, player : PlayerClass):
        event_queue.registerHandler("event_end", self.eventHandler)
        self.player=player
        self.widgetList = [urwid.Text(["Health:", str(self.player['health'])])]
        super().__init__(self.widgetList)
        self._selectable=False
    def getSize(self):
        return (len(self.widget_list)+1, 4*len(self.widget_list[0].get_text())+2)
    def __del__(self):
        event_queue.unregisterHandler("event_end", self.eventHandler)
    def render(self, size, focus = False):
        self.update()
        return super().render(size, focus)
