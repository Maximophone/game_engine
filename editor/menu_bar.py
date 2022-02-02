import imgui

from observers.event_system import EventSystem
from observers.events.event import Event
from observers.events.event_type import EventType

class MenuBar:
    def imgui(self):
        imgui.begin_main_menu_bar()
        if imgui.begin_menu("File"):
            if imgui.menu_item("Save", "Ctrl+S")[0]:
                EventSystem.notify(None, Event(EventType.SaveLevel))
            if imgui.menu_item("Load", "Ctrl+O")[0]:
                EventSystem.notify(None, Event(EventType.LoadLevel))
            imgui.end_menu()
        imgui.end_main_menu_bar()