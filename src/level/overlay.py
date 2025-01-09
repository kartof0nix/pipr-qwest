import urwid
from src.globals import player
from src.common import event_queue

class overlayWidget(urwid.Pile):
    def update(self):
        self.widgetList[0].set_text([('hred', "Health:  "), str(player.player['health'])]),
        self.widgetList[1].set_text([('hgreen', "Attack:  "), str(player.player.calcAttack() )]),
        self.widgetList[2].set_text([('hblue', "Defense:  "), str(player.player.calcDefense() )])

    async def eventHandler(self, params=None):
        self._invalidate()
    def __init__(self):
        event_queue.registerHandler("event_end", self.eventHandler)
        event_queue.registerHandler("event_change", self.eventHandler)
        self.widgetList = [urwid.Text("") for i in range(3)]
        self.update()
        super().__init__(self.widgetList)
        self._selectable=False
    def __del__(self):
        event_queue.unregisterHandler("event_end", self.eventHandler)
        event_queue.registerHandler("event_change", self.eventHandler)
    def render(self, size, focus = False):
        self.update()
        return super().render(size, focus)
