from pyrr import Vector3
from components.component import Component
from util.settings import Settings

import numpy as np

class GridLines(Component):
    def editor_update(self, dt: float):
        from mxeng.window import Window
        from renderer.debug_draw import DebugDraw

        camera = Window.get_scene().camera()
        camera_pos = camera.position
        projection_size = camera.projection_size

        first_x = (camera_pos[0] // Settings.GRID_WIDTH - 1) * Settings.GRID_WIDTH
        first_y = (camera_pos[1] // Settings.GRID_HEIGHT - 1) * Settings.GRID_HEIGHT

        num_vert_lines = int(projection_size[0] * camera.zoom / Settings.GRID_WIDTH) + 2
        num_horiz_lines = int(projection_size[1] * camera.zoom / Settings.GRID_HEIGHT) + 2
        
        width = int(projection_size[0] * camera.zoom) + Settings.GRID_WIDTH * 2
        height = int(projection_size[1] * camera.zoom) + Settings.GRID_HEIGHT * 2

        max_lines = max(num_vert_lines, num_horiz_lines)
        color = Vector3([0.2, 0.2, 0.2])
        for i in range(max_lines):
            x = first_x + Settings.GRID_WIDTH * i
            y = first_y + Settings.GRID_HEIGHT * i

            if i < num_vert_lines:
                DebugDraw.add_line_2D(np.array([x, first_y]), np.array([x, first_y+height]), color)

            if i < num_horiz_lines:
                DebugDraw.add_line_2D(np.array([first_x, y]), np.array([first_x+width, y]), color)