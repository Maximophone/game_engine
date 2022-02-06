from openal import oalStream, oalQuit, oalOpen
import openal.al as al

class Sound:
    def __init__(self, filepath: str, loops: bool):
        self.buffer_id: int = 0
        self.source_id: int = 0
        self.filepath: str = filepath
        self._is_playing: bool = False

        self.source_stream = oalOpen(filepath)#oalStream(filepath)

    def delete(self):
        oalQuit()

    def play(self):
        if not self.is_playing:
            self.source_stream.position = 0
            self.source_stream.play()
            self._is_playing = True

    def stop(self):
        if self._is_playing:
            self.source_stream.stop()
            self._is_playing = False

    @property
    def is_playing(self):
        if self.source_stream.get_state() == al.AL_STOPPED:
            self._is_playing = False
        return self._is_playing