from visual_arr import *

class stackOrderMap(visualArrOrderMap):
    def set_ini(self, subtype, datas:list):
        self.datastruct.node_set(datas[0], datas[1], datas[2], int(datas[3]), float(datas[4]))
        self.datastruct.size = float(datas[4])
        self.datastruct.get_boundary()

    def change_ini(self, subtype, datas: list):
        if subtype == 1:
            self.datastruct.change(-1, datas[1])


class VisualStack(VisualArr):
    size = 0.6
    node_type = Node.Node()
    datatype = stackOrderMap

    def get_boundary(self):
        g = Group(
            Line(3 * UP, 3 * DOWN, color=GREEN),
            Line(self.size * LEFT, self.size * RIGHT, color=GREEN),
            Line(3 * UP, 3 * DOWN, color=GREEN),
        )
        g.arrange(RIGHT, buff=0)
        g[1].move_to(DOWN * 3)
        for shape in g:
            self.add(shape)
            self.wait(0.1)

    def row_play(self, st, end, x_start, x_gap, y=RIGHT + LEFT):
        if end - st <= 0:
            return None
        for i in range(st, end):
            cur = self.objs_arr[i]
            cur.generate_target()
            cur.target.move_to(y + x_start)
            x_start += x_gap

    def push(self, x):
        self.label("Push: " + str(x))

        n = self.objs_arr.__len__()
        self.objs_arr.append(self.node_type.put(x).move_to(3.5*UP+LEFT))
        self.play(self.objs_arr[n].animate.shift(RIGHT))
        self.arrange(n)


    def pop(self):
        self.erase(self.objs_arr.__len__() - 1)

    def erase(self, i):
        self.label("Pop")
        n = self.objs_arr.__len__()
        if n == 0:
            return None
        n -= 1
        self.play(self.objs_arr[i].animate.move_to(3.5*UP))
        self.play(self.objs_arr[i].animate.shift(RIGHT))
        self.play(FadeOut(self.objs_arr[i]))
        self.objs_arr.remove(self.objs_arr[i])

        if n == 0:
            return None

        self.arrange(n - 1)

    def arrange(self, m):
        start = (3 - 0.6*self.size)*DOWN

        n = self.objs_arr.__len__()

        self.row_play(0, n, start, (self.size+0.1*self.size) * UP)
        if n > 0:
            self.play(
                AnimationGroup(
                    *[
                        MoveToTarget(cur)
                        for cur in self.objs_arr
                    ]
                )
            )
        return start
    def label(self, msg):
        if self.showLabel:
            tmp = Text(msg).move_to(3*LEFT)
            self.play(Write(tmp))
            self.play(FadeOut(tmp))

    def init(self, arr: list):
        n = arr.__len__()
        m = n - 1
        start = (3 - 0.6 * self.size) * DOWN
        for i in range(0, n):
            self.objs_arr.append(self.node_type.put(arr[i]).move_to(start))
            start += (0.1*self.size + self.size) * UP

        if n > 0:
            self.play(
                AnimationGroup(
                    *[
                        FadeIn(cur)
                        for cur in self.objs_arr
                    ],
                    lag_ratio=0.1
                )
            )