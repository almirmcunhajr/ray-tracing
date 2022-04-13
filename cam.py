import itertools
from typing import List, Set, Tuple
import numpy as np

from .object import Object
class Cam:
    def __init__(
        self,
        v_res: int,
        h_res: int,
        s: int,
        d: int,
        e: np.ndarray,
        l: np.ndarray,
        up: np.ndarray,

        background_color: np.ndarray,
        objects: List[Object]
    ) -> None:
        self.v_res = v_res
        self.h_res = h_res
        self.s = s
        self.d = d
        self.e = e
        self.l = l
        self.up = up

        self.background_color = background_color
        self.objects = objects
    
    def render(self) -> np.ndarray:
        img = np.array([[np.array([0, 0, 0])]*self.h_res]*self.v_res)

        w = self.e-self.l
        w = w/np.linalg.norm(w)

        u = np.cross(self.up, w)
        u = u/np.linalg.norm(u)

        v = np.cross(w, u)

        for (i, j) in itertools.product(range(self.v_res), range(self.h_res)):
            x = self.s*(j-(self.h_res/2)+0.5)
            y = self.s*(i-(self.v_res/2)+0.5)

            q = self.e+(x*u)+(y*v)-(self.d*self.w)
            q = q/np.linalg.norm(q)

            img[i][j] = self.cast(self.e, q)
    
    def cast(self, o: np.ndarray, d: np.ndarray) -> np.ndarray:
        c = self.background_color
        s = self.trace(o, d)
        if len(s) != 0:
            t, closest = min(s)
            c = closest.color
        return c

    def trace(self, o: np.ndarray, d: np.ndarray) -> Set[Tuple[int, Object]]:
        s = set()
        for obj in self.objects:
            t = obj.intersection(o, d)
            if t:
                s.add((t, obj))
        return s
