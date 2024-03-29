from typing import Dict, List
from components.spritesheet import Spritesheet
from mxeng.sound import Sound
from renderer.shader import Shader
from renderer.texture import Texture
from pathlib import Path

class AssetPool:
    _shaders: Dict[str, Shader] = {}
    _textures: Dict[str, Texture] = {}
    _spritesheets: Dict[str, Spritesheet] = {}
    _sounds: Dict[str, Sound] = {}

    @staticmethod
    def get_shader(resource_name: str) -> Shader:
        resource_path = str(Path(resource_name).absolute())
        if resource_path in AssetPool._shaders:
            return AssetPool._shaders[resource_path]
        else:
            shader = Shader(resource_path)
            shader.compile()
            AssetPool._shaders[resource_path] = shader
            return shader

    @staticmethod
    def get_texture(resource_name: str) -> Texture:
        resource_path = str(Path(resource_name).absolute())
        if resource_path in AssetPool._textures:
            return AssetPool._textures[resource_path]
        else:
            texture = Texture(resource_path)
            AssetPool._textures[resource_path] = texture
            return texture

    @staticmethod
    def add_spritesheet(resource_name: str, spritesheet: Spritesheet):
        resource_path = str(Path(resource_name).absolute())
        if resource_path not in AssetPool._spritesheets:
            AssetPool._spritesheets[resource_path] = spritesheet
    
    @staticmethod
    def get_spritesheet(resource_name: str) -> Spritesheet:
        resource_path = str(Path(resource_name).absolute())
        if resource_path not in AssetPool._spritesheets:
            assert False, f"Tried to access spritesheet {resource_name} and it has not been added to the asset pool"
        return AssetPool._spritesheets.get(resource_path)

    @staticmethod
    def get_sound(sound_file: str) -> Sound:
        resource_path = str(Path(sound_file).absolute())
        if resource_path in AssetPool._sounds:
            return AssetPool._sounds[resource_path]
        assert False, f"Tried to access sound {sound_file} and it has not been added yet"

    @staticmethod
    def add_sound(sound_file: str, loops: bool) -> Sound:
        resource_path = str(Path(sound_file).absolute())
        if resource_path in AssetPool._sounds:
            return AssetPool._sounds[resource_path]
        else:
            sound = Sound(resource_path, loops)
            AssetPool._sounds[resource_path] = sound
            return sound

    @staticmethod
    def get_all_sounds() -> List[Sound]:
        return list(AssetPool._sounds.values())