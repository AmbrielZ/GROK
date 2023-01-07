from visual_arr import *


class VisualQueue(VisualArr):
    showLabel = 1
    size=0.4
    node_type = Node.Node(node_type="Cycle", node_size=size)


    def init_ini(self, subtype, datas:list):
        self.get_boundary()


    def row_play(self, st, end, x_start, x_gap, y=UP + DOWN):
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
        self.objs_arr.append(self.node_type.put(x).move_to(4*RIGHT))
        self.arrange(n)


    def pop(self):
        self.erase(0)

    def erase(self, i):
        self.label("Pop")
        n = self.objs_arr.__len__()
        if n == 0:
            return None
        n -= 1
        self.play(self.objs_arr[i].animate.move_to(5 * LEFT))
        self.play(FadeOut(self.objs_arr[i]))
        self.objs_arr.remove(self.objs_arr[i])

        if n == 0:
            return None

        self.arrange(n - 1)


    def arrange(self, m):
        start = (4.5+self.size)* LEFT
        n = self.objs_arr.__len__()

        self.row_play(0, n, start, (self.size+0.1)*RIGHT)
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
            tmp = Text(msg).move_to(UP + (0 if self.objs_arr.__len__() == 0 else self.objs_arr[0].get_y()))
            self.play(Write(tmp))
            self.play(FadeOut(tmp))

    def get_boundary(self):
        g = Group(
            Line(5.5 * LEFT, 5.5 * RIGHT, color=GREEN),
            Line(5.5 * LEFT, 5.5 * RIGHT, color=GREEN),
        )
        g[0].move_to(self.size * DOWN)
        g[1].move_to(self.size * UP)
        for shape in g:
            self.add(shape)
            self.wait(0.1)
