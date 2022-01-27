import imgui
from imgui.integrations.glfw import GlfwRenderer

from scenes.scene import Scene

class ImGUILayer:
    impl = None
    font = None

    @staticmethod
    def init_imgui(glfw_window):
        imgui.create_context()
        ImGUILayer.impl = GlfwRenderer(glfw_window)

        io = imgui.get_io()
        # io.fonts.clear_fonts()
        ImGUILayer.font = io.fonts.add_font_from_file_ttf(
            "assets/fonts/consola.ttf", 32
        )

        ImGUILayer.impl.refresh_font_texture()

    @staticmethod
    def update(dt: float, scene: Scene):
        ImGUILayer.impl.process_inputs()

        imgui.new_frame()
        scene.scene_imgui()
        with imgui.font(ImGUILayer.font):
            if imgui.begin_main_menu_bar():
                if imgui.begin_menu("File", True):

                    clicked_quit, selected_quit = imgui.menu_item(
                        "Quit", 'Cmd+Q', False, True
                    )

                    if clicked_quit:
                        exit(1)

                    imgui.end_menu()
                imgui.end_main_menu_bar()

            imgui.begin("First window", True)
            imgui.text("Hello world!")
            imgui.end()
        
        imgui.render()
        ImGUILayer.impl.render(imgui.get_draw_data())

    @staticmethod
    def shutdown():
        ImGUILayer.impl.shutdown()


