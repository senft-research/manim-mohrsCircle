import numpy as np
from manim import BLUE, Dot, RED, VGroup, Circle, MathTex, UP, DOWN, Line, ParametricFunction, TAU
from manim.utils.color.DVIPSNAMES import CYAN


class Points:
    def __init__(self, p1, p2):
        self.point_1 = p1
        self.point_2 = p2


def init_points(stress_x, stress_y, stress_shear):
    p1 = np.array([stress_x, -stress_shear, 0])
    p2 = np.array([stress_y, stress_shear, 0])
    return Points(p1, p2)


class MohrCircle(VGroup):
    def __init__(self, stress_x, stress_y, stress_shear, axes, **kwargs):
        super().__init__(**kwargs)
        self.axes = axes
        self._init_stresses(stress_x, stress_y, stress_shear)
        self._create_objects()
        self._set_mobject_z_indices()
        self._add_mobjects()

    def _init_stresses(self, stress_x, stress_y, stress_shear):
        self.stress_x = stress_x
        self.stress_y = stress_y
        self.stress_shear = stress_shear

    def _create_objects(self):
        self._create_dots()
        self.line = Line(self.point_1.get_center(), self.point_2.get_center(), color=BLUE)
        self._create_labels()
        self._create_circle()

    def _create_dots(self):
        self.point_1 = Dot(point=self.axes.c2p(self.stress_x, -self.stress_shear), color=CYAN)
        self.point_2 = Dot(point=self.axes.c2p(self.stress_y, self.stress_shear), color=CYAN)

    def _create_labels(self):
        self.label_1 = MathTex(f"({self.stress_x}, {-self.stress_shear})").next_to(self.point_1, UP)
        self.label_2 = MathTex(f"({self.stress_y}, {self.stress_shear})").next_to(self.point_2, DOWN)

    def _create_circle(self):
        points = init_points(
            self.stress_x,
            self.stress_y,
            self.stress_shear
        )

        self._init_key_geometry(points)
        
        self.circle = ParametricFunction(
            lambda t: self.axes.c2p(self._create_circle_points(t)
            ),
            t_range=[0, TAU],
            color=RED,
        )
        self._rotate_circle(points)

    def _add_mobjects(self):
        self.add(self.circle)
        self.add(self.point_1, self.point_2)
        self.add(self.label_1, self.label_2)
        self.add(self.line)

    def _set_mobject_z_indices(self):
        self.circle.set_z_index(0)
        self.line.set_z_index(1)
        self.point_1.set_z_index(2)
        self.point_2.set_z_index(2)

    def _init_key_geometry(self, points):
        self.center_point = (points.point_1 + points.point_2) / 2
        self.circle_radius = np.linalg.norm(
            points.point_1 - points.point_2
        ) / 2

    def _create_circle_points(self,t):
        return (self.center_point[0] + self.circle_radius * np.cos(t),
        self.center_point[1] + self.circle_radius * np.sin(t))

    def _rotate_circle(self, points):
        angle = self._find_point_angle(points)
        self.circle.rotate(angle, about_point=self.circle.get_center())

    def _find_point_angle(self, points):
        p1 = points.point_1[:2]
        center = self.center_point[:2]
        return float(np.arctan2(
            p1[1] - center[1],
            p1[0] - center[0]
        ))
