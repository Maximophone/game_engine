import glfw
import OpenGL.GL as gl
from mxeng.game_object import GameObject
from mxeng.imgui_layer import ImGUILayer
from mxeng.key_listener import KeyListener
from mxeng.mouse_listener import MouseListener
from observers.event_system import EventSystem
from observers.events.event import Event
from observers.events.event_type import EventType
from physics2d.physics2d import Physics2D
from renderer.framebuffer import Framebuffer
from renderer.picking_texture import PickingTexture
from renderer.renderer import Renderer
from mario.scenes.level_scene_initializer import LevelSceneInitializer
from scenes.scene import Scene
from mario.scenes.level_editor_scene_initializer import LevelEditorSceneInitializer
from scenes.scene_initializer import SceneInitializer
from util.asset_pool import AssetPool
from util.timer import Time
import ctypes

import openal.al as al
import openal.alc as alc

class Window:
    _window = None
    def __init__(self, width: int = 1920, height: int = 1080, title: str = "MxEng"):
        self._width = width
        self._height = height
        self._title = title
        self.glfw_window = None
        self.framebuffer: Framebuffer = None
        self.picking_texture: PickingTexture = None
        self.r = 1
        self.b = 1
        self.g = 1
        self.a = 1

        self.current_scene: Scene = None
        self._queued_scene: SceneInitializer = None
        self.imgui_layer = None

        self._level_editor_initializer: type = None
        self._level_initializer: type = None

        self.runtime_play: bool = False
        
        # Initialise audio device
        default_device_name = alc.alcGetString(0, alc.ALC_DEFAULT_DEVICE_SPECIFIER)
        self.audio_device = alc.alcOpenDevice(default_device_name)
        attributes = 0
        self.audio_context: int = alc.alcCreateContext(self.audio_device, ctypes.c_long(attributes))
        alc.alcMakeContextCurrent(self.audio_context)

        EventSystem.add_observer(self)

    @property
    def editor_mode(self) -> bool:
        return self._level_editor_initializer is not None

    @staticmethod
    def change_scene(scene_initializer: SceneInitializer):
        if Window.get_scene() is not None:
            Window.get_scene().destroy()

        Window.get_imgui_layer().properties_window.active_game_object = None
        Window.get().current_scene = Scene(scene_initializer)
        Window.get().current_scene.load()
        Window.get().current_scene.init()
        Window.get().current_scene.start()

    @staticmethod
    def queue_change_scene(scene_initializer: SceneInitializer):
        Window.get()._queued_scene = scene_initializer

    @staticmethod
    def get_scene() -> Scene:
        return Window.get().current_scene

    @staticmethod
    def get_physics() -> Physics2D:
        return Window.get_scene().physics

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
    def get_framebuffer() -> Framebuffer:
        return Window.get().framebuffer

    @staticmethod
    def get_target_aspect_ratio() -> float:
        return 16./9.

    @staticmethod
    def get_imgui_layer() -> ImGUILayer:
        return Window.get().imgui_layer

    @staticmethod
    def resize_callback(window, w: int, h: int):
        Window.get()._width = w
        Window.get()._height = h

    def run(self, level_initializer: type, level_editor_initalizer: type = None):
        self._level_initializer = level_initializer
        self._level_editor_initializer = level_editor_initalizer
        self.init()
        self.loop()

        # Destroy the audio context
        alc.alcDestroyContext(self.audio_context)
        alc.alcCloseDevice(self.audio_device)

        # Free the memory
        self.imgui_layer.shutdown()
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

        
        # Enable v-sync
        glfw.swap_interval(1)
        glfw.show_window(self.glfw_window)

        # TODO: Missing GL.createCapabilities()

        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_ONE, gl.GL_ONE_MINUS_SRC_ALPHA)

        self.framebuffer = Framebuffer(2560, 1440)
        self.picking_texture = PickingTexture(2560, 1440)
        self.imgui_layer = ImGUILayer(self.picking_texture)
        # Important: this initialisation needs to happen before the mouse callbacks are added
        self.imgui_layer.init_imgui(self.glfw_window)

        # Register Mouse callbacks
        glfw.set_cursor_pos_callback(self.glfw_window, MouseListener.mouse_pos_callback)
        glfw.set_mouse_button_callback(self.glfw_window, MouseListener.mouse_button_callback)
        glfw.set_scroll_callback(self.glfw_window, MouseListener.mouse_scroll_callback)
        glfw.set_key_callback(self.glfw_window, KeyListener.key_callback)
        glfw.set_window_size_callback(self.glfw_window, Window.resize_callback)
        
        gl.glViewport(0, 0, 2560, 1440)

        Window.change_scene(self._level_editor_initializer() if self.editor_mode else self._level_initializer())

    def loop(self):
        from renderer.debug_draw import DebugDraw
        begin_time: float = Time.get_time()
        end_time: float = Time.get_time()
        dt: float = -1

        default_shader = AssetPool.get_shader("assets/shaders/default.glsl")
        picking_shader = AssetPool.get_shader("assets/shaders/picking_shader.glsl")

        while not glfw.window_should_close(self.glfw_window):
            glfw.poll_events()

            if self.editor_mode:
                # Render pass 1: render to picking texture
                gl.glDisable(gl.GL_BLEND)
                self.picking_texture.enable_writing()

                gl.glViewport(0, 0, 2560, 1440)
                gl.glClearColor(0., 0., 0., 0.)
                gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

                Renderer.bind_shader(picking_shader)
                self.current_scene.render()

                self.picking_texture.disable_writing()
                gl.glEnable(gl.GL_BLEND)

                # Render pass 2: render actual game
                DebugDraw.begin_frame()

                gl.glClearColor(self.r, self.g, self.b, self.a)
                gl.glClear(gl.GL_COLOR_BUFFER_BIT)

                self.framebuffer.bind()

                gl.glClearColor(*Window.get_scene().camera().clear_color)
                gl.glClear(gl.GL_COLOR_BUFFER_BIT)

                if dt >= 0:
                    Renderer.bind_shader(default_shader)
                    if self.runtime_play:
                        self.current_scene.update(dt)
                    else:
                        self.current_scene.editor_update(dt)
                    DebugDraw.draw()
                    self.current_scene.render()
                self.framebuffer.unbind()
                    
                self.imgui_layer.update(dt, self.current_scene)
            else:

                gl.glClearColor(*Window.get_scene().camera().clear_color)
                gl.glClear(gl.GL_COLOR_BUFFER_BIT)

                if dt >= 0:
                    Renderer.bind_shader(default_shader)
                    self.current_scene.update(dt)
                    self.current_scene.render()

            if self._queued_scene is not None:
                self.change_scene(self._queued_scene)
                self._queued_scene = None

            KeyListener.end_frame()
            MouseListener.end_frame()
            glfw.swap_buffers(self.glfw_window)

            end_time = Time.get_time()
            dt = end_time - begin_time
            begin_time = end_time

            fps = 1/dt
            #print(f"Running at {fps:.2f} FPS")

    def on_notify(self, go: GameObject, event: Event):
        if event.type == EventType.GameEngineStartPlay:
            self.runtime_play = True
            self.current_scene.save()
            Window.change_scene(self._level_initializer())
        elif event.type == EventType.GameEngineStopPlay:
            self.runtime_play = False
            Window.change_scene(self._level_editor_initializer())
        elif event.type == EventType.LoadLevel:
            Window.change_scene(self._level_editor_initializer())
        elif event.type == EventType.SaveLevel:
            self.current_scene.save()