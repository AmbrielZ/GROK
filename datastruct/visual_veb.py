from manim import *
import Node


class veb(MovingCameraScene):
    node_type = Node.Node(node_type="RoundedSquare", node_size=0.6)

    def construct(self):
        # it = self.node_type.put_label(0, '[' + str(0) + ',' + str(15) + ']', DOWN, 1)
        # self.play(Create(it))
        it = self.node_type.put_label(20, 'Max', UP)
        c0 = self.node_type.get_font('Cluster', 1.2).move_to(self.node_type.node_s*DOWN).shift(1.5*LEFT)
        it1 = self.node_type.put_label(10, 'Min', UP).shift(1.5*LEFT)
        it3 = self.node_type.put_label(0, 'Summary', UP, 1.5).shift(2.25*RIGHT)
        VGroup(c0, it, it1, it3).shift(0.75 * LEFT + 0.5*UP)
        sur = RoundedRectangle(width=6, height=3)
        objs = VGroup()
        start = LEFT + RIGHT
        for i in range(0, 4):
            objs.add(self.node_type.put(1).move_to(c0.get_center()+DOWN*self.node_type.node_s + start))
            start += RIGHT*1.5
        b = self.camera.frame.height
        c = self.camera.frame.get_center()
        all = VGroup(c0, it, it1, it3, sur, objs)
        self.play(FadeIn(all))
        self.wait(1)
        self.play(AnimationGroup(*[self.camera.auto_zoom(objs[1][0]), FadeOut(all)],  lag_ratio=0.2))
        self.camera.frame.height = b
        self.camera.frame.move_to(c)
        self.play(FadeIn(all))


