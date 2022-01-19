from typing import Dict
from renderer.shader import Shader
from renderer.texture import Texture
from pathlib import Path

class AssetPool:
    _shaders: Dict[str, Shader] = {}
    _textures: Dict[str, Texture] = {}

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