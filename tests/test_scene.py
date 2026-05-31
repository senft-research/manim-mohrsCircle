from manim import *

from manim_mohrscircle import MohrCircle

class TestScene(MovingCameraScene):
    def construct(self):
        stress_x = 5
        stress_y = 2
        stress_shear = 2
        axes = Axes(
            x_range=[-3, 8, 1],
            y_range=[-3, 8, 1],
            x_length=8,
            y_length=8,
            axis_config={"include_numbers": True},
        )
        mc = MohrCircle(stress_x, stress_y, stress_shear, axes)
        self.add(mc.axes)
        self.camera.frame.move_to(mc.circle.get_center())
        self.play(
            FadeIn(mc.point_1_dot),
            FadeIn(mc.point_2_dot),
            FadeIn(mc.center_point_dot),
            FadeIn(mc.label_1),
            FadeIn(mc.label_2),
            lag_ratio=0.3
        )
        self.wait(2)
        self.play(Create(mc.line))
        self.play(Create(mc.circle), run_time=2)
        self.wait(1)
        self.play(FadeIn(mc.max_stress_dot), run_time=2)
        self.play(FadeIn(mc.min_stress_dot), run_time=2)
        self.play(FadeIn(mc.max_shear_dot), run_time=2)
        self.play(FadeIn(mc.min_shear_dot), run_time=2)
        self.play(FadeIn(mc.find_stress_point_at_element_rotation_degrees(45)), run_time=2)