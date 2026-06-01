from typing import Iterable

import numpy as np
from manim import BLUE, Dot, RED, VGroup, Circle, MathTex, Line, WHITE, RIGHT, VMobject
from manim.utils.color.DVIPSNAMES import CYAN

## TODO Need to add better label formatting, code cleanup (maybe separate classes for different functionality?) and add
##      nice animations (such as a protractor line for circle creation)
class Points:
    def __init__(self, p1, p2):
        self.point_1 = p1
        self.point_2 = p2
        self.center_point = (p1 + p2) / 2
## TODO still not perfect, would like to make the font size potentialy dynamic? Also give user some options? Need to look
##      into kwargs a bit more
class MohrCirclePoint(VGroup):
    def __init__(self, stress_x, stress_y, axes, label_kwargs = None, *vmobjects: VMobject | Iterable[VMobject], **kwargs):
        super().__init__(*vmobjects, **kwargs)
        dot = Dot(point=axes.c2p([stress_x, stress_y]), color=CYAN)
        label_kwargs = label_kwargs or {}
        label = MathTex(f"({stress_x}, {stress_y})", **label_kwargs).next_to(dot, RIGHT)
        self.point_center = dot.get_center()
        self.add(dot)
        self.add(label)



def init_points(stress_x, stress_y, stress_shear):
    p1 = np.array([stress_x, -stress_shear, 0])
    p2 = np.array([stress_y, stress_shear, 0])
    return Points(p1, p2)


class MohrCircle(VGroup):
    def __init__(self, stress_x, stress_y, stress_shear, axes, point_label_kwargs = None, **kwargs):
        super().__init__(**kwargs)
        self.point_label_kwargs = point_label_kwargs or {}

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
        self.line = Line(self.point_1_dot.point_center, self.point_2_dot.point_center, color=BLUE)
        self._create_circle()

    def _create_initial_dots(self):
        self.point_1_dot = MohrCirclePoint(self.circle_points.point_1[0], self.circle_points.point_1[1], self.axes, self.point_label_kwargs)
        self.point_2_dot = MohrCirclePoint(self.circle_points.point_2[0], self.circle_points.point_2[1], self.axes, self.point_label_kwargs)
        self.center_point_dot = Dot(point=self.axes.c2p(self.circle_points.center_point), color=RED)
        self.min_stress_dot = Dot(point=self.axes.c2p(np.array([self.min_stress_x, 0, 0])), color=CYAN)
        self.max_stress_dot = Dot(point=self.axes.c2p(np.array([self.max_stress_x, 0, 0])), color=CYAN)
        self.min_shear_dot = Dot(point=self.axes.c2p(np.array([self.center_point[0], self.min_shear_y, 0])), color=CYAN)
        self.max_shear_dot = Dot(point=self.axes.c2p(np.array([self.center_point[0], self.max_shear_y, 0])), color=CYAN)


    def _create_circle(self):
        self.circle = Circle(radius=(float(self.scene_circle_radius)))
        self.circle.move_to(self.center_point_dot.get_center())
        self._rotate_circle()

    def _add_mobjects(self):
        self.add(self.axes)
        self.add(self.circle)
        self.add(self.point_1_dot, self.point_2_dot)
        self.add(self.line)
        self.add(self.center_point_dot)

    def _set_mobject_z_indices(self):
        self.circle.set_z_index(0)
        self.line.set_z_index(1)
        self.point_1_dot.set_z_index(2)
        self.point_2_dot.set_z_index(2)
        self.center_point_dot.set_z_index(2)

    def _init_key_geometry(self):
        self.center_point = self.circle_points.center_point
        self.circle_radius = np.linalg.norm(
            self.circle_points.point_1 - self.circle_points.point_2
        ) / 2

        self.scene_center_point = self.axes.c2p(*self.circle_points.center_point)

        p1_scene = self.axes.c2p(*self.circle_points.point_1)
        p2_scene = self.axes.c2p(*self.circle_points.point_2)
        self.scene_circle_radius = np.linalg.norm(p1_scene - p2_scene) / 2

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

    def find_stress_point_at_element_rotation_rads(self, rot_angle_rads):
        stress_point = self.circle.point_at_angle(rot_angle_rads*2)
        return Dot(point=stress_point, color=WHITE)

    def find_stress_point_at_element_rotation_degrees(self, rot_angle_degrees):

        return self.find_stress_point_at_element_rotation_rads(rot_angle_degrees*(np.pi/180))