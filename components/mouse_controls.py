from enum import unique
from components.component import Component
from components.non_pickable import NonPickable
from components.sprite_renderer import SpriteRenderer
from components.state_machine import StateMachine
from mxeng.game_object import GameObject
from mxeng.key_listener import KeyListener
from mxeng.mouse_listener import MouseListener

import glfw

from util.settings import Settings
from util.vectors import Color3, Color4, Vector2


class MouseControls(Component):
    def __init__(self):
        self.holding_object: GameObject = None
        self.debounce_time = 0.2
        self.debounce = self.debounce_time
        self.box_select_set = False
        self.box_select_start = Vector2()
        self.box_select_end = Vector2()
        super().__init__()

    def pickup_object(self, go: GameObject):
        from mxeng.window import Window
        if self.holding_object is not None:
            self.holding_object.destroy()
        self.holding_object = go
        self.holding_object.get_component(SpriteRenderer).set_color(Color4([0.8, 0.8, 0.8, 0.5]))
        self.holding_object.add_component(NonPickable())
        Window.get_scene().add_game_object_to_scene(go)

    def place(self):
        from mxeng.window import Window
        new_obj = self.holding_object.copy()
        if new_obj.get_component(StateMachine) is not None:
            new_obj.get_component(StateMachine).refresh_textures()
        new_obj.get_component(SpriteRenderer).set_color(Color4([1., 1., 1., 1.]))
        new_obj.remove_component(NonPickable)
        Window.get_scene().add_game_object_to_scene(new_obj)

    def editor_update(self, dt: float):
        from mxeng.window import Window
        from renderer.debug_draw import DebugDraw
        self.debounce -= dt
        picking_texture = Window.get_imgui_layer().properties_window.picking_texture
        
        if self.holding_object is not None:
            self.holding_object.transform.position.x = MouseListener.get_world_x()
            self.holding_object.transform.position.y = MouseListener.get_world_y()
            self.holding_object.transform.position.x = (self.holding_object.transform.position.x // Settings.GRID_WIDTH) * Settings.GRID_WIDTH + Settings.GRID_WIDTH/2
            self.holding_object.transform.position.y = (self.holding_object.transform.position.y // Settings.GRID_HEIGHT) * Settings.GRID_HEIGHT + Settings.GRID_HEIGHT/2

            if MouseListener.mouse_button_down(glfw.MOUSE_BUTTON_LEFT):
                half_width = Settings.GRID_WIDTH / 2.
                half_height = Settings.GRID_HEIGHT / 2.
                if MouseListener.is_dragging() and not self.block_in_square(
                    self.holding_object.transform.position.x - half_width,
                    self.holding_object.transform.position.y - half_height
                    ):
                    self.place()
                elif not MouseListener.is_dragging() and self.debounce < 0:
                    self.place()
                    self.debounce = self.debounce_time

            if KeyListener.is_key_pressed(glfw.KEY_ESCAPE):
                self.holding_object.destroy()
                self.holding_object = None
        elif not MouseListener.is_dragging() and MouseListener.mouse_button_down(glfw.MOUSE_BUTTON_LEFT) and self.debounce < 0:
            x = MouseListener.get_screen_x()
            y = MouseListener.get_screen_y()
            #print(MouseListener.get()._game_viewport_pos)
            #print(MouseListener.get_x(), MouseListener.get_y())
            #print(MouseListener.get_screen_x(), MouseListener.get_screen_y())
            if x<-1 or x>1 or y<-1 or y>1:
                return
            game_object_id = picking_texture.read_pixel((x+1)/2.*2560, (y+1)/2.*1440) # HACK
            picked_object = Window.get_scene().get_game_object(game_object_id)
            if picked_object is not None and picked_object.get_component(NonPickable) is None:
                Window.get_imgui_layer().properties_window.active_game_object = picked_object
            elif picked_object is None:
                Window.get_imgui_layer().properties_window.clear_selected()
            self.debounce = 0.2
        elif MouseListener.is_dragging() and MouseListener.mouse_button_down(glfw.MOUSE_BUTTON_LEFT):
            if not self.box_select_set:
                Window.get_imgui_layer().properties_window.clear_selected()
                self.box_select_start = MouseListener.get_screen()
                self.box_select_set = True
            self.box_select_end = MouseListener.get_screen()
            box_select_start_world = MouseListener.screen_to_world(self.box_select_start)
            box_select_end_world = MouseListener.screen_to_world(self.box_select_end)
            half_size = (box_select_end_world - box_select_start_world)*.5
            #print("Drawing box Screen: ", self.box_select_start, self.box_select_end)
            #print("Drawing box World: ", box_select_start_world, box_select_end_world)
            #DebugDraw.add_box_2D(Vector2([0.5, 0.5]), Vector2([0.7, 0.7]), color=Color3([1., 0., 0.]))
            DebugDraw.add_box_2D(box_select_start_world + half_size, half_size*2., color=Color3([0.1, 0.9, 0]), lifetime=1)
        elif self.box_select_set:
            self.box_select_set = False
            #TODO: can't have this conversion here...
            screen_start_x = int((self.box_select_start.x+1)/2*2560)
            screen_start_y = int((self.box_select_start.y+1)/2*1440)
            screen_end_x = int((self.box_select_end.x+1)/2*2560)
            screen_end_y = int((self.box_select_end.y+1)/2*1440)

            self.box_select_start = Vector2()
            self.box_select_end = Vector2()

            if screen_end_x < screen_start_x:
                tmp = screen_start_x
                screen_start_x = screen_end_x
                screen_end_x = tmp
            if screen_end_y < screen_start_y:
                tmp = screen_start_y
                screen_start_y = screen_end_y
                screen_end_y = tmp

            game_object_ids = picking_texture.read_pixels(Vector2([screen_start_x, screen_start_y]), Vector2([screen_end_x, screen_end_y]))
            unique_game_object_ids = set()
            for game_object_id in game_object_ids:
                unique_game_object_ids.add(int(game_object_id))

            for game_object_id in unique_game_object_ids:
                picked_object = Window.get_scene().get_game_object(game_object_id)
                if picked_object is not None and picked_object.get_component(NonPickable) is None:
                    Window.get_imgui_layer().properties_window.add_active_game_object(picked_object)

    def block_in_square(self, x: float, y: float) -> bool:
        from mxeng.window import Window
        properties_window = Window.get_imgui_layer().properties_window
        start = Vector2([x, y])
        end = start + Vector2([Settings.GRID_WIDTH, Settings.GRID_HEIGHT])
        start_screen_f = MouseListener.world_to_screen(start)
        end_screen_f = MouseListener.world_to_screen(end)
        # TODO: Fix bug, it seems like objects below are being detected
        # To reproduce, place a horizontal line of objects by dragging, then place
        # another line above it
        start_screen_i = Vector2([int(start_screen_f.x) + 2, int(start_screen_f.y) + 2])
        end_screen_i = Vector2([int(end_screen_f.x) - 2, int(end_screen_f.y) - 2])
        game_object_ids = properties_window.picking_texture.read_pixels(start_screen_i, end_screen_i)
        
        for game_object_id in game_object_ids:
            if game_object_id > 0:
                picked_object = Window.get_scene().get_game_object(int(game_object_id))
                if picked_object.get_component(NonPickable) is None:
                    return True
        return False


