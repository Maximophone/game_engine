from util.vectors import Vector2

import imgui


class MXImGUI:
    DEFAULT_COLUMN_WIDTH: float = 220.
    @staticmethod
    def draw_vec2_control(label: str, values: Vector2, reset_value: float = 0., column_width: float = DEFAULT_COLUMN_WIDTH):
        imgui.push_id(label)
        imgui.columns(2)
        imgui.set_column_width(0, column_width)
        imgui.text(label)
        imgui.next_column()

        imgui.push_style_var(imgui.STYLE_ITEM_SPACING, (0, 0))
        line_height = imgui.get_font_size() + imgui.get_style().frame_padding.y * 2.
        button_size = Vector2([line_height + 3., line_height])
        width_each = (imgui.calculate_item_width() - button_size.x * 2.) / 2.

        imgui.push_item_width(width_each)
        imgui.push_style_color(imgui.COLOR_BUTTON, 0.8, 0.1, 0.15, 1.)
        imgui.push_style_color(imgui.COLOR_BUTTON_HOVERED, 0.9, 0.2, 0.2, 1.)
        imgui.push_style_color(imgui.COLOR_BUTTON_ACTIVE, 0.8, 0.1, 0.15, 1.)
        if imgui.button("X", button_size.x, button_size.y):
            values.x = reset_value
        imgui.pop_style_color(3)
        imgui.same_line()
        _, values.x = imgui.drag_float("##x", values.x, 0.1)
        imgui.pop_item_width()

        imgui.same_line()
        imgui.push_item_width(width_each)
        imgui.push_style_color(imgui.COLOR_BUTTON, 0.1, 0.8, 0.15, 1.)
        imgui.push_style_color(imgui.COLOR_BUTTON_HOVERED, 0.2, 0.9, 0.2, 1.)
        imgui.push_style_color(imgui.COLOR_BUTTON_ACTIVE, 0.1, 0.8, 0.15, 1.)
        if imgui.button("Y", button_size.x, button_size.y):
            values.y = reset_value
        imgui.pop_style_color(3)
        imgui.same_line()
        _, values.y = imgui.drag_float("##y", values.y, 0.1)
        imgui.pop_item_width()
        imgui.same_line()

        imgui.next_column()

        imgui.pop_style_var()
        imgui.columns(1)
        imgui.pop_id()

    @staticmethod
    def drag_float(label: str, value: float) -> float:
        imgui.push_id(label)
        imgui.columns(2)
        imgui.set_column_width(0, MXImGUI.DEFAULT_COLUMN_WIDTH)
        imgui.text(label)
        imgui.next_column()

        _, new_value = imgui.drag_float("##drag_float", value, 0.1)

        imgui.columns(1)
        imgui.pop_id()

        return new_value

    @staticmethod
    def drag_int(label: str, value: int) -> int:
        imgui.push_id(label)
        imgui.columns(2)
        imgui.set_column_width(0, MXImGUI.DEFAULT_COLUMN_WIDTH)
        imgui.text(label)
        imgui.next_column()

        _, new_value = imgui.drag_int("##drag_int", value, 0.1)

        imgui.columns(1)
        imgui.pop_id()

        return new_value

    @staticmethod
    def input_text(label: str, text: str) -> str:
        imgui.push_id(label)
        imgui.columns(2)
        imgui.set_column_width(0, MXImGUI.DEFAULT_COLUMN_WIDTH)
        imgui.text(label)
        imgui.next_column()

        _, out_string = imgui.input_text("##text_input", text, 256)

        imgui.columns(1)
        imgui.pop_id()

        return out_string