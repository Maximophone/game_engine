import glfw
import OpenGL.GL as gl
from mxeng.imgui_layer import ImGUILayer
from mxeng.key_listener import KeyListener
from mxeng.mouse_listener import MouseListener
from renderer.framebuffer import Framebuffer
from scenes.scene import Scene
from scenes.level_editor_scene import LevelEditorScene
from scenes.level_scene import LevelScene
from util.timer import Time

class Window:
    _window = None
    def __init__(self, width: int = 1920, height: int = 1080, title: str = "Hello World"):
        self._width = width
        self._height = height
        self._title = title
        self.glfw_window = None
        self.framebuffer: Framebuffer = None
        self.r = 1
        self.b = 1
        self.g = 1
        self.a = 1

        self.current_scene: Scene = None

    @staticmethod
    def change_scene(new_scene: int):
        if new_scene == 0:
            Window.get().current_scene = LevelEditorScene()
        elif new_scene == 1:
            Window.get().current_scene = LevelScene()
        else:
            assert False, f"Unknown scene: {new_scene}"
        Window.get().current_scene.load()
        Window.get().current_scene.init()
        Window.get().current_scene.start()

    @staticmethod
    def get_scene() -> Scene:
        return Window.get().current_scene

    @staticmethod
    def get():
        if Window._window is None:
            Window._window = Window()

        return Window._window

    @staticmethod
    def get_width() -> int:
        #return Window.get()._width
        return glfw.get_window_size(Window.get().glfw_window)[0]

    @staticmethod
    def get_height() -> int:
        #return Window.get()._height
        return glfw.get_window_size(Window.get().glfw_window)[1]

    @staticmethod
    def resize_callback(window, w: int, h: int):
        Window.get()._width = w
        Window.get()._height = h

    def run(self):
        self.init()
        self.loop()

        # Free the memory
        ImGUILayer.shutdown()
        glfw.destroy_window(self.glfw_window)

        glfw.terminate()

    def init(self):
        assert glfw.init(), "Unable to initialize GLFW"

        # Configure GLFW
        glfw.default_window_hints()
        glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
        glfw.window_hint(glfw.RESIZABLE, glfw.TRUE)
        glfw.window_hint(glfw.MAXIMIZED, glfw.TRUE)

        # Create the window
        self.glfw_window = glfw.create_window(self._width, self._height, self._title, None, None)
        if not self.glfw_window:
            glfw.terminate()
            assert False, "Window failed to create"
        
        glfw.make_context_current(self.glfw_window)

        # Important: this initialisation needs to happen before the mouse callbacks are added
        ImGUILayer.init_imgui(self.glfw_window)

        # Register Mouse callbacks
        glfw.set_cursor_pos_callback(self.glfw_window, MouseListener.mouse_pos_callback)
        glfw.set_mouse_button_callback(self.glfw_window, MouseListener.mouse_button_callback)
        glfw.set_scroll_callback(self.glfw_window, MouseListener.mouse_scroll_callback)
        glfw.set_key_callback(self.glfw_window, KeyListener.key_callback)
        glfw.set_window_size_callback(self.glfw_window, Window.resize_callback)
        
        # Enable v-sync
        glfw.swap_interval(1)
        glfw.show_window(self.glfw_window)

        # TODO: Missing GL.createCapabilities()

        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_ONE, gl.GL_ONE_MINUS_SRC_ALPHA)

        self.framebuffer = Framebuffer(2560, 1440)

        Window.change_scene(0)

    def loop(self):
        from renderer.debug_draw import DebugDraw
        begin_time: float = Time.get_time()
        end_time: float = Time.get_time()
        dt: float = -1

        while not glfw.window_should_close(self.glfw_window):
            glfw.poll_events()

            DebugDraw.begin_frame()

            gl.glClearColor(self.r, self.g, self.b, self.a)
            gl.glClear(gl.GL_COLOR_BUFFER_BIT)

            self.framebuffer.bind()
            if dt >= 0:
                DebugDraw.draw()
                self.current_scene.update(dt)
            self.framebuffer.unbind()
                
            ImGUILayer.update(dt, self.current_scene)
            glfw.swap_buffers(self.glfw_window)

            end_time = Time.get_time()
            dt = end_time - begin_time
            begin_time = end_time

            fps = 1/dt
            # print(f"Running at {fps:.2f} FPS")

        self.current_scene.save_exit()
