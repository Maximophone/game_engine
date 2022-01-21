import imgui
from imgui.integrations.glfw import GlfwRenderer

class ImGUILayer:
    impl = None

    @staticmethod
    def init_imgui(glfw_window):
        imgui.create_context()
        ImGUILayer.impl = GlfwRenderer(glfw_window)

    @staticmethod
    def update(dt: float):
        ImGUILayer.impl.process_inputs()

        imgui.new_frame()

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


