from pyrr import Vector3, Vector4

class Vector2(Vector3):
    def __new__(cls, values=None, *args, **kwargs):
        values = values if values is not None else [0, 0]
        return super().__new__(cls, [*values, 0], *args, **kwargs)

    @classmethod
    def from_vector3(cls, vector, dtype=None):
        return Vector2(vector[:2], dtype=dtype if dtype is not None else vector.dtype)

class Color3(Vector3):
    pass

class Color4(Vector4):
    pass