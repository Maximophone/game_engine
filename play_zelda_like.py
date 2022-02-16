from zelda_like.scenes.level_editor import LevelEditorSceneInitializer
from zelda_like.scenes.level import LevelSceneInitializer

from mxeng.window import Window
import sys

if __name__ == "__main__":
    window = Window.get()
    if len(sys.argv) == 1:
        window.run(LevelSceneInitializer, LevelEditorSceneInitializer)
    else:
        window.run(LevelSceneInitializer)