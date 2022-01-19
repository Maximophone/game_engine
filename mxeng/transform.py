import numpy as np

class Transform:
    def __init__(self, position = None, scale = None):
        self.position = position if position is not None else np.array([0.,0.])
        self.scale = scale if scale is not None else np.array([1.,1.])