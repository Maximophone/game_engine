from mario.scenes.level_editor_scene_initializer import LevelEditorSceneInitializer
from mario.scenes.level_scene_initializer import LevelSceneInitializer
from mxeng.window import Window
import sys

if __name__ == "__main__":
    window = Window.get()
    if len(sys.argv) == 1:
        window.run(LevelSceneInitializer, LevelEditorSceneInitializer)
    else:
        window.run(LevelSceneInitializer)