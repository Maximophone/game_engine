import imgui
from util.vectors import Vector2
from mxeng.window import Window

class GameViewWindow:
    @staticmethod
    def imgui():
        imgui.begin("Game Viewport", imgui.WINDOW_NO_SCROLLBAR | imgui.WINDOW_NO_SCROLL_WITH_MOUSE)
        window_size = GameViewWindow.get_largest_size_for_viewport()
        window_pos = GameViewWindow.get_centered_position_for_viewport(window_size)

        imgui.core.set_cursor_pos([window_pos.x, window_pos.y])
        texture_id = Window.get_framebuffer().texture_id
        imgui.core.image(texture_id, window_size.x, window_size.y, (0, 1), (1, 0))

        imgui.end()

    @staticmethod
    def get_largest_size_for_viewport() -> Vector2:
        window_size = Vector2(imgui.core.get_content_region_available())
        window_size.x -= imgui.core.get_scroll_x()
        window_size.y -= imgui.core.get_scroll_y()

        aspect_width = window_size.x
        aspect_height = aspect_width / Window.get_target_aspect_ratio()
        if aspect_height > window_size.y:
            # we must swith to pillarbox mode
            aspect_height = window_size.y
            aspect_width = aspect_height * Window.get_target_aspect_ratio()

        return Vector2([aspect_width, aspect_height])


    @staticmethod
    def get_centered_position_for_viewport(aspect_size: Vector2) -> Vector2:
        window_size = Vector2(imgui.core.get_content_region_available())
        window_size.x -= imgui.core.get_scroll_x()
        window_size.y -= imgui.core.get_scroll_y()

        viewport_x = window_size.x / 2.0 - aspect_size.x / 2.0
        viewport_y = window_size.y / 2.0 - aspect_size.y / 2.0

        return Vector2([viewport_x + imgui.core.get_cursor_pos_x(), viewport_y + imgui.core.get_cursor_pos_y()])