import imgui
from mxeng.mouse_listener import MouseListener
from util.vectors import Vector2
from mxeng.window import Window

from observers.event_system import EventSystem
from observers.events.event import Event
from observers.events.event_type import EventType

class GameViewWindow:
    def __init__(self):
        self.left_x, self.right_x, self.top_y, self.bottom_y = 0., 0., 0., 0.
        self.is_playing: bool = False

    def imgui(self):
        imgui.begin("Game Viewport", flags=imgui.WINDOW_NO_SCROLLBAR | imgui.WINDOW_NO_SCROLL_WITH_MOUSE | imgui.WINDOW_NO_MOVE | imgui.WINDOW_MENU_BAR)
        
        imgui.begin_menu_bar()
        if imgui.menu_item("Play", None, self.is_playing, not self.is_playing)[0]:
            self.is_playing = True
            EventSystem.notify(None, Event(EventType.GameEngineStartPlay))
        if imgui.menu_item("Stop", None, not self.is_playing, self.is_playing)[0]:
            self.is_playing = False
            EventSystem.notify(None, Event(EventType.GameEngineStopPlay))
        imgui.end_menu_bar()
        
        imgui.set_cursor_pos([imgui.get_cursor_pos().x, imgui.get_cursor_pos().y])
        window_size = self.get_largest_size_for_viewport()
        window_pos = self.get_centered_position_for_viewport(window_size)
        imgui.set_cursor_pos([window_pos.x, window_pos.y])

        #HACK: why these offsets??
        self.left_x = window_pos.x  + 60
        self.right_x = window_pos.x + window_size.x + 60
        self.bottom_y = window_pos.y + 60
        self.top_y = window_pos.y + window_size.y + 60

        texture_id = Window.get_framebuffer().texture_id
        imgui.image(texture_id, window_size.x, window_size.y, (0, 1), (1, 0))

        MouseListener.set_game_viewport_pos(Vector2([self.left_x, self.bottom_y]))
        MouseListener.set_game_viewport_size(window_size.copy())

        imgui.end()

    def get_want_capture_mouse(self):
        return (
            MouseListener.get_x() >= self.left_x and
            MouseListener.get_x() <= self.right_x and
            MouseListener.get_y() >= self.bottom_y and
            MouseListener.get_y() <= self.top_y
        )

    def get_largest_size_for_viewport(self) -> Vector2:
        window_size = Vector2(imgui.get_content_region_available())

        aspect_width = window_size.x
        aspect_height = aspect_width / Window.get_target_aspect_ratio()
        if aspect_height > window_size.y:
            # we must swith to pillarbox mode
            aspect_height = window_size.y
            aspect_width = aspect_height * Window.get_target_aspect_ratio()

        return Vector2([aspect_width, aspect_height])


    def get_centered_position_for_viewport(self, aspect_size: Vector2) -> Vector2:
        window_size = Vector2(imgui.get_content_region_available())

        viewport_x = window_size.x / 2.0 - aspect_size.x / 2.0
        viewport_y = window_size.y / 2.0 - aspect_size.y / 2.0

        return Vector2([viewport_x + imgui.get_cursor_pos_x(), viewport_y + imgui.get_cursor_pos_y()])
