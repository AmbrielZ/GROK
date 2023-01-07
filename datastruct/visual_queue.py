from visual_arr import *
class queueOrderMap(visualArrOrderMap):
    def set_ini(self, subtype, datas:list):
        self.datastruct.node_set(datas[0], datas[1], datas[2], int(datas[3]), float(datas[4]))
        self.datastruct.size = float(datas[4])
        self.datastruct.get_boundary()

class VisualQueue(VisualArr):
    showLabel = 1
    size = 0.7
    node_type = Node.Node()
    datatype = queueOrderMap

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
        self.play(self.objs_arr[i].animate.move_to(5.5 * LEFT))
        self.play(FadeOut(self.objs_arr[i]))
        self.objs_arr.remove(self.objs_arr[i])

        if n == 0:
            return None

        self.arrange(n - 1)

    def arrange(self, m):
        start = (4.5+self.size) * LEFT
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

    def init(self, arr: list):
        n = arr.__len__()
        start = (4.5 + self.size) * LEFT
        for i in range(0, n):
            self.objs_arr.append(self.node_type.put(arr[i]).move_to(start))
            start += (self.size+0.1)*RIGHT

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

