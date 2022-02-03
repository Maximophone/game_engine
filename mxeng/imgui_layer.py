import imgui
from imgui.integrations.glfw import GlfwRenderer
from editor.menu_bar import MenuBar
from editor.properties_window import PropertiesWindow
from editor.scene_hierarchy_window import SceneHierarchyWindow
from renderer.picking_texture import PickingTexture

from scenes.scene import Scene

class ImGUILayer:
    def __init__(self, picking_texture: PickingTexture):
        self.impl = None
        self.font = None
        self._properties_window: PropertiesWindow = PropertiesWindow(picking_texture)
        self._scene_hierarchy_window: SceneHierarchyWindow = SceneHierarchyWindow()
        self._menu_bar: MenuBar = MenuBar()

    @property
    def properties_window(self):
        return self._properties_window

    def init_imgui(self, glfw_window):
        imgui.create_context()
        self.impl = GlfwRenderer(glfw_window)

        io = imgui.get_io()
        # io.fonts.clear_fonts()
        self.font = io.fonts.add_font_from_file_ttf(
            "assets/fonts/consola.ttf", 32
        )

        self.impl.refresh_font_texture()

    def update(self, dt: float, scene: Scene):
        from editor.game_view_window import GameViewWindow
        self.impl.process_inputs()

        imgui.new_frame()
        # ImGUILayer.setup_dock_space()
        scene.imgui()
       # with imgui.font(self.font):
        self._menu_bar.imgui()
        # imgui.end()
        
        GameViewWindow.imgui()
        self._properties_window.update(dt, scene)
        self._properties_window.imgui()
        self._scene_hierarchy_window.imgui()
        imgui.render()
        self.impl.render(imgui.get_draw_data())

    def setup_dock_space(self):
        # Can't implement for now because docking is not ported to pyimgui
        from mxeng.window import Window
        imgui.core.set_next_window_position(0., 0.)
        imgui.core.set_next_window_size(Window.get_width(), Window.get_height)

    def shutdown(self):
        self.impl.shutdown()


