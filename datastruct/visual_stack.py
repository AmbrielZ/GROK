from visual_arr import *

class VisualStack(VisualArr):
    size = 0.6
    node_type = Node.Node(node_type="Cycle", node_size=size)
    def _set(self):
        self.order_map = {
            1: self.init_ini,
            3: self.push_ini,
            4: self.pop_ini
        }

    def init_ini(self, subtype, datas:list):
        self.get_boundary()

    def push_ini(self, subtype, datas: list):
        self.push(datas[0])

    def pop_ini(self, subtype, datas: list):
        self.pop()

    def read_from(self):
        fi = open(Node.path)
        for line in fi.readlines():
            print(line)
            ret = line.split()
            act_type = int(ret[0])
            act_subtype = int(ret[1])
            if act_type == -1:
                break
            self.order_map[act_type](
                act_subtype,
                [
                    int(ret[i])
                    for i in range(2, ret.__len__())
                ]
            )
        self.wait(3)

    def construct(self):
        # self.label(1)
        self._set()
        self.showLabel = 1
        self.read_from()
        return None


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
