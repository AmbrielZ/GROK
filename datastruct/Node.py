from manim import *
CYAN = "#00FFFF"
PK = "#FF7AB2"

'''
2.0
node_form 新增了圆角矩形
Node类里新增了put_label方法, 可以生成带label的节点(可以用来做线段树)
Node类里的put_font更名为get_font, 以后put类方法指返回节点的方法
TreeNode类还没完全设计完, x轴基本完毕, 但y轴还没
'''


def node_form_num(x, font_color=CYAN, node_color=PK, node_size=0.5):
    return VGroup(Tex(str(x), color=font_color, font_size=0.5*node_size*font_size_map[str(x).__len__()]))


def node_form_cycle(x, font_color=CYAN, node_color=PK, node_size=0.5):
    return VGroup(
        Tex(str(x), color=font_color, font_size=0.5*node_size*font_size_map[str(x).__len__()]),
        Circle(color=node_color, radius=0.5*node_size)
    )


def node_form_square(x, font_color=WHITE, node_color=ORANGE, node_size=0.5):
    return VGroup(
        Tex(str(x), color=font_color, font_size=0.5*node_size*font_size_map[str(x).__len__()]),
        Square(color=node_color, side_length=node_size)
    )


def node_form_roundedsquare(x, font_color=WHITE, node_color=ORANGE, node_size=0.5):
    return VGroup(
        Tex(str(x), color=font_color, font_size=0.5*node_size*font_size_map[str(x).__len__()]),
        RoundedRectangle(color=node_color, width=node_size, height=node_size, corner_radius=0.2*node_size)
    )


path = "../grok_to_manim"

node_type_map = {"Cycle": node_form_cycle, "Square": node_form_square,
                 "RoundedSquare": node_form_roundedsquare ,"Num": node_form_num}

font_size_map = {1: 160, 2: 130, 3: 110, 4: 90, 5: 70, 6: 60, 7: 50, 8: 40}


class Node:
    def __init__(self, font_color=CYAN, node_color=PK, node_size=0.8, node_type="Cycle"):
        self.font_c = font_color
        self.node_c = node_color
        self.node_s = node_size
        self.node_t = node_type_map[node_type]

    def put(self, x):
        return self.node_t(x, self.font_c, self.node_c, self.node_s)

    def put_label(self, x, _lab=None, pos=UP, prop=0.7):
        return VGroup(
            self.node_t(x, self.font_c, self.node_c, self.node_s),
            self.get_font(x if _lab is None else _lab, prop).move_to(pos * self.node_s)
        )

    def get_font(self, x, prop=0.5):
        return Tex(str(x), color=self.font_c, font_size=prop*self.node_s*font_size_map[str(x).__len__()])


class TreeNode(VGroup):

    def __init__(self, mobj, left=-5.0, right=5.0, prop=1.2):
        self.left = left
        self.right = right
        self.child = list()
        self.prop = prop
        print(left, right, self.get_x_position())
        super(TreeNode, self).__init__(mobj.move_to(RIGHT * self.get_x_position()).scale(prop))

    def align_points_with_larger(self, larger_mobject):
        pass

    def get_x_position(self):
        return (self.left + self.right) / 2.0

    def get_child_position(self, div=2):
        start = self.left
        gap = (self.right - self.left) / div
        ans = []
        for i in range(0, div):
            ans.append(list([start, start + gap]))
            start += gap
        return ans

    def shift_tree(self, vec=UP):
        for ch in self.child:
            ch.shift_tree(vec)
        return self.shift(vec)

    def animate_shift_tree(self, vec=UP):
        return AnimationGroup(self.animate.shift(vec), *[ch.animate_shift_tree(vec) for ch in self.child])

    def re_div(self, left, right, y):
        self.left = left
        self.right = right
        return self.move_to(self.get_x_position()*RIGHT + y * UP)

    def insert(self, x, node_type):
        n = self.child.__len__()
        pos = self.get_child_position(n + 1)
        it = TreeNode(
            node_type.put(x),
            pos[n][0],
            pos[n][1],
            self.prop*0.9
            # 越下层越小，系数待定
        )
        self.child.append(it)

        y_pos = self.get_y() - 1.5*self.prop
        # 越下层间隔越近， 方程待定

        return AnimationGroup(
            *[
                self.child[i].animate.re_div(pos[i][0], pos[i][1], y_pos)
                for i in range(0, n + 1)
            ],
            Create(it.move_to(it.get_x()*RIGHT + y_pos*UP))
        )
