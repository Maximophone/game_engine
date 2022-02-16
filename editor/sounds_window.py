from typing import List
import imgui
from pathlib import Path

from mxeng.sound import Sound

class SoundsWindow:
    def __init__(self, sounds: List[Sound]):
        self.sounds: List[Sound] = sounds

    def imgui(self):
        imgui.begin("Sounds")
        for i, sound in enumerate(self.sounds):
            sound_path = sound.filepath
            if imgui.button(Path(sound_path).name):
                if not sound.is_playing:
                    sound.play()

                else:
                    sound.stop()
            if i%5:
                imgui.same_line()

        imgui.end()