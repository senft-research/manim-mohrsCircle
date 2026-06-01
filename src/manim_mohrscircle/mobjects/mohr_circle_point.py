from typing import Iterable

from manim import VGroup, VMobject, Dot, MathTex, RIGHT
from manim.utils.color.DVIPSNAMES import CYAN


class MohrCirclePoint(VGroup):
    def __init__(self, stress_x, stress_y, axes, label_kwargs = None, *vmobjects: VMobject | Iterable[VMobject], **kwargs):
        super().__init__(*vmobjects, **kwargs)
        label_kwargs = label_kwargs or {}
        label_kwargs.setdefault("font_size", 30)

        dot = Dot(point=axes.c2p([stress_x, stress_y]), color=CYAN)
        label = MathTex(f"({stress_x}, {stress_y})", **label_kwargs).next_to(dot, RIGHT)
        self.point_center = dot.get_center()
        self.add(dot)
        self.add(label)
