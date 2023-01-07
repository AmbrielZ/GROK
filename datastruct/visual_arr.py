from manim import *
import Node

# 默认 0为无值 1为单值/双值 2为多值 3为重复多值
# -1 over
# 1 init
# 2 change
# 3 push_back
# 4 pop_back
# 5 insert
# 6 erase
# 7 swap
# 8 clear

class visualArrOrderMap(Node.orderMap):
    def ini(self, datastruct):
        self.datastruct = datastruct
        self.set(0, self.set_ini)
        self.set(1, self.init_ini)
        self.set(2,self.change_ini)
        self.set(3,self.push_ini)
        self.set(4,self.pop_ini)
        self.set(5,self.insert_ini)
        self.set(6,self.erase_ini)
        self.set(7,self.swap_ini)
        self.set(8,self.clear_ini)

    def init_ini(self, subtype, datas: list):
        if subtype == 3:
            self.datastruct.init(datas)
        elif subtype == 4:
            self.datastruct.init([datas[1] for i in range(0, int(datas[0]))])

    def change_ini(self, subtype, datas: list):
        if subtype == 1:
            self.datastruct.change(int(datas[0]), datas[1])

    def push_ini(self, subtype, datas: list):
        self.datastruct.push(datas[0])

    def pop_ini(self, subtype, datas: list):
        self.datastruct.pop()

    def insert_ini(self, subtype, datas: list):
        if subtype == 1:
            self.datastruct.insert(int(datas[0]), datas[1])
        elif subtype == 2:
            for i in range(1, datas.__len__()):
                self.datastruct.insert(int(datas[0])  + i - 1, datas[i])
        # elif subtype == 3:

    def erase_ini(self, subtype, datas: list):
        if subtype == 1:
            self.datastruct.erase(int(datas[0]))

    def swap_ini(self, subtype, datas: list):
        self.datastruct.swap(int(datas[0]), int(datas[1]))

    def clear_ini(self, subtype, datas: list):
        self.datastruct.clear()

    def set_ini(self, subtype, datas:list):
        self.datastruct.node_set(datas[0], datas[1], datas[2], int(datas[3]), float(datas[4]))

class VisualArr(Scene):
    objs_arr = []
    showLabel = 0
    node_type = Node.Node()
    reader = Node.reader()
    datatype = visualArrOrderMap

    def node_set(self, node_type ="Circle", font_color = Node.CYAN, node_color = Node.PK, label = 0, node_size = 0.8):
        print(node_size)
        self.node_type.__init__(font_color=font_color, node_color=node_color, node_size=node_size, node_type=node_type)
        self.showLabel = label

    def _set(self):
        order_map = self.datatype()
        order_map.ini(self)
        self.reader.__int__(order_map=order_map)

    def construct(self):
        self._set()
        self.reader.read_from()
        self.wait()

    def push(self, x):
        self.label("Push: " + str(x))

        n = self.objs_arr.__len__()

        self.objs_arr.append(self.node_type.put(x).move_to(self.arrange(n)))
        self.play(Create(self.objs_arr[n]))

    def pop(self):
        self.erase(self.objs_arr.__len__() - 1)

    def insert(self, i, x):
        self.label("Insert: " + str(x) + " to " + "[ " + str(i) + " ]")

        n = self.objs_arr.__len__()
        start = ((n + 1) >> 1) * LEFT
        gap = ((n + 1.0) / n if n & 1 else 1) * RIGHT
        k = start + i * gap
        for cur in self.objs_arr:
            if start[0] == k[0] and start[1] == k[1]:
                start += gap
            cur.generate_target()
            cur.target.move_to(start)
            start += gap
        self.play(
            AnimationGroup(
                *[
                    MoveToTarget(cur)
                    for cur in self.objs_arr
                ]
            )
        )
        self.objs_arr.insert(i, self.node_type.put(x).move_to(k + DOWN))
        self.play(FadeIn(self.objs_arr[i]))
        self.play(self.objs_arr[i].animate.move_to(k))

    def erase(self, i):
        self.label("Erase: " + "[ " + str(i) + " ]")

        n = self.objs_arr.__len__()
        if n == 0:
            return None
        n -= 1

        self.play(FadeOut(self.objs_arr[i]))
        self.objs_arr.remove(self.objs_arr[i])

        if n == 0:
            return None

        self.arrange(n - 1)

    def swap(self, i, j):
        if i == j:
            return None
        lb = "     Swap: [" + str(i) + "]and[" + str(j) + "]"
        self.label(lb)

        self.play(CyclicReplace(self.objs_arr[i], self.objs_arr[j]))
        self.objs_arr[i], self.objs_arr[j] = self.objs_arr[j], self.objs_arr[i]

    def change(self, i, x):
        self.label("Change: " + "[ " + str(i) + " ]" + " to " + str(x))
        self.play(Transform(
            self.objs_arr[i][0],
            self.node_type.get_font(x).move_to(self.objs_arr[i].get_center())
        ))

    def clear(self):
        if self.objs_arr.__len__() > 0:
            self.play(
                AnimationGroup(
                    *[
                        FadeOut(cur)
                        for cur in self.objs_arr
                    ]
                )
            )
            self.objs_arr = []

    def highlight(self, i):
        self.play(self.objs_arr[i].animate.scale(1.25), run_time=0.4)
        self.play(self.objs_arr[i].animate.scale(0.8), run_time=0.5)

    def label(self, msg):
        if self.showLabel:
            tmp = Text(msg).move_to(UP + (0 if self.objs_arr.__len__() == 0 else self.objs_arr[0].get_y()))
            self.play(Write(tmp))
            self.play(FadeOut(tmp))

    def init(self, arr: list):
        n = arr.__len__()
        m = n - 1
        start = ((m + 1) >> 1) * LEFT

        for i in range(0, n):
            self.objs_arr.append(self.node_type.put(arr[i]).move_to(start))
            start += ((m + 1.0) / m if m & 1 else 1) * RIGHT

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

    def arrange(self, m):
        start = ((m + 1) >> 1) * LEFT
        n = self.objs_arr.__len__()

        self.row_play(0, n, start, ((m + 1.0) / m if m & 1 else 1) * RIGHT)
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

    def row_play(self, st, end, x_start, x_gap, y=UP + DOWN):
        if end - st <= 0:
            return None
        for i in range(st, end):
            cur = self.objs_arr[i]
            cur.generate_target()
            cur.target.move_to(y + x_start)
            x_start += x_gap