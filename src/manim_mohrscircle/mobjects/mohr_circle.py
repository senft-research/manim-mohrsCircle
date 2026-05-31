import numpy as np
from manim import BLUE, Dot, RED, VGroup, Circle, MathTex, UP, DOWN, Line, ParametricFunction, TAU
from manim.utils.color.DVIPSNAMES import CYAN

## TODO Need to add better label formatting, maybe do some sort of rotating line / protractor animation when creating
##      the circle, add way to show the principle stresses / max & min shear stresses, and how to show stresses at specific
##      angle.
class Points:
    def __init__(self, p1, p2):
        self.point_1 = p1
        self.point_2 = p2
        self.center_point = (p1 + p2) / 2


def init_points(stress_x, stress_y, stress_shear):
    p1 = np.array([stress_x, -stress_shear, 0])
    p2 = np.array([stress_y, stress_shear, 0])
    return Points(p1, p2)


class MohrCircle(VGroup):
    def __init__(self, stress_x, stress_y, stress_shear, axes, **kwargs):
        super().__init__(**kwargs)
        self.axes = axes
        self._init_raw_data(stress_x, stress_y, stress_shear)
        self._create_objects()
        self._set_mobject_z_indices()
        self._add_mobjects()

    def _init_raw_data(self, stress_x, stress_y, stress_shear):
        self.stress_x = stress_x
        self.stress_y = stress_y
        self.stress_shear = stress_shear
        self.circle_points = init_points(
            self.stress_x,
            self.stress_y,
            self.stress_shear
        )
        self._init_key_geometry()
        self._find_principle_stresses()
        self._find_shear_stress_boundaries()


    def _create_objects(self):
        self._create_initial_dots()
        self.line = Line(self.point_1_dot.get_center(), self.point_2_dot.get_center(), color=BLUE)
        self._create_labels()
        self._create_circle()

    def _create_initial_dots(self):
        self.point_1_dot = Dot(point=self.axes.c2p(self.circle_points.point_1), color=CYAN)
        self.point_2_dot = Dot(point=self.axes.c2p(self.circle_points.point_2), color=CYAN)
        self.center_point_dot = Dot(point=self.axes.c2p(self.circle_points.center_point), color=RED)
        self.min_stress_dot = Dot(point=self.axes.c2p(np.array([self.min_stress_x, 0, 0])), color=CYAN)
        self.max_stress_dot = Dot(point=self.axes.c2p(np.array([self.max_stress_x, 0, 0])), color=CYAN)
        self.min_shear_dot = Dot(point=self.axes.c2p(np.array([self.center_point[0], self.min_shear_y, 0])), color=CYAN)
        self.max_shear_dot = Dot(point=self.axes.c2p(np.array([self.center_point[0], self.max_shear_y, 0])), color=CYAN)

    def _create_labels(self):
        self.label_1 = MathTex(f"({self.stress_x}, {-self.stress_shear})").next_to(self.point_1_dot, UP)
        self.label_2 = MathTex(f"({self.stress_y}, {self.stress_shear})").next_to(self.point_2_dot, DOWN)

    def _create_circle(self):

        self.circle = ParametricFunction(
            lambda t: self.axes.c2p(self._create_circle_points(t)
            ),
            t_range=[0, TAU],
            color=RED,
        )

        self._rotate_circle()

    def _add_mobjects(self):
        self.add(self.circle)
        self.add(self.point_1_dot, self.point_2_dot)
        self.add(self.label_1, self.label_2)
        self.add(self.line)
        self.add(self.center_point_dot)

    def _set_mobject_z_indices(self):
        self.circle.set_z_index(0)
        self.line.set_z_index(1)
        self.point_1_dot.set_z_index(2)
        self.point_2_dot.set_z_index(2)
        self.center_point_dot.set_z_index(2)
        self.label_1.set_z_index(3)
        self.label_2.set_z_index(3)

    def _init_key_geometry(self):
        self.center_point = self.circle_points.center_point
        self.circle_radius = np.linalg.norm(
            self.circle_points.point_1 - self.circle_points.point_2
        ) / 2

    def _create_circle_points(self,t):
        return (self.center_point[0] + self.circle_radius * np.cos(t),
                self.center_point[1] + self.circle_radius * np.sin(t))

    def _rotate_circle(self):
        angle = self._find_point_angle(self.circle_points)
        self.circle.rotate(angle, about_point=self.circle.get_center())

    def _find_point_angle(self, points):
        p1 = points.point_1[:2]
        center = self.center_point[:2]
        return float(np.arctan2(
            p1[1] - center[1],
            p1[0] - center[0]
        ))

    def _find_principle_stresses(self):
        center_x = self.circle_points.center_point[0]
        self.min_stress_x = center_x - self.circle_radius
        self.max_stress_x = center_x + self.circle_radius

    def _find_shear_stress_boundaries(self):
        center_y = self.circle_points.center_point[1]
        self.min_shear_y = center_y - self.circle_radius
        self.max_shear_y = center_y + self.circle_radius

