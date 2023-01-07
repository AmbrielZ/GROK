from manim import *
import random
CYAN = "#00FFFD"
PK = "#FF7AB2"
RD = "#DF0000"


def get_rand_color():
    ret = '#'
    color_div = {
        10: 'A', 11: 'B', 12: 'C',
        13: 'D', 14: 'E', 15: 'F'
    }
    for cur in range(10):
        color_div[cur] = str(cur)
    for cur in range(6):
        ret += color_div[random.randint(0, 15)]
    return ret

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

node_type_map = {"Circle": node_form_cycle, "Square": node_form_square,
                 "RoundedSquare": node_form_roundedsquare,"Num": node_form_num}


font_size_map = {1: 160, 2: 130, 3: 110, 4: 90, 5: 70, 6: 60, 7: 50, 8: 40}


class Node:
    def __init__(self, font_color=CYAN, node_color=PK, node_size=0.8, node_type="Circle"):
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

    def put_labels(self, x, _lab, pos, prop):
        n = pos.__len__()
        return VGroup(
            self.node_t(x, self.font_c, self.node_c, self.node_s),
            *[self.get_font(x if _lab is None else _lab[i], prop[i]).move_to(pos[i] * self.node_s) for i in range(0, n)]
        )

    def get_font(self, x, prop=0.5):
        return Tex(str(x), color=self.font_c, font_size=prop*self.node_s*font_size_map[str(x).__len__()])

class orderMap:
    order_map = {}
    datastruct = None

    def __getitem__(self, item):
        return self.order_map[item]

    def ini(self, datastruct):
        self.datastruct = datastruct

    def set(self, i, func):
        self.order_map[i] = func

class reader:
    def __int__(self, order_map):
        self.order = order_map

    def read_from(self):
        global path
        fi = open(path)
        for line in fi.readlines():
            ret = line.split()
            act_type = int(ret[0])
            act_subtype = int(ret[1])
            if act_type == -1:
                break
            self.order[act_type](
                act_subtype,
                [
                    ret[i]
                    for i in range(2, ret.__len__())
                ]
            )

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

    def animate_shift_tree(self, vec=UP):
        return AnimationGroup(self.animate.shift(vec), *[ch.animate_shift_tree(vec) for ch in self.child])

    def re_div(self, left, right, y):
        self.left = left
        self.right = right
        return self.move_to(self.get_x_position()*RIGHT + y * UP)

    def push(self, x, node_type):
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

        y_pos = self.get_y() - 1.2*self.prop
        # 越下层间隔越近， 方程待定

        return AnimationGroup(
            *[
                self.child[i].animate.re_div(pos[i][0], pos[i][1], y_pos)
                for i in range(0, n + 1)
            ],
            Create(it.move_to(it.get_x()*RIGHT + y_pos*UP))
        )

class BinaryTreeNode(VGroup):

    def align_points_with_larger(self, larger_mobject):
        pass

    small_prop = 0.9
    show_branch = True

    def __init__(self, mobj, y_pos=0.0, left=-5.0, right=5.0, prop=1.0, branch=True):
        self.show_branch = branch
        # 节点的x由left和right界定
        self.left = left
        self.right = right

        # 二叉树节点的子节点
        self.l_child = None
        self.r_child = None
        self.prop = prop

        super().__init__(mobj.move_to(RIGHT * self.get_x_pos() + UP * y_pos).scale(prop))

    def change(self, y, node_type):
        pos = self.submobjects[0][0].get_center()
        self.submobjects[0][0] = node_type.get_font(y).move_to(pos)

    def get_x_pos(self):
        return (self.left + self.right) / 2.0

    def get_l_xrange(self):
        return [self.left, self.get_x_pos()]

    def get_r_xrange(self):
        return [self.get_x_pos(), self.right]

    def get_child_ypos(self):
        return self.get_real_y() - 1.2*self.prop

    def get_parent_ypos(self):
        return 1.2*self.prop/self.small_prop + self.get_real_y()

# 以下方法用于新增节点和改变整个树位置
    def set_l(self, x, node_type):
        self.l_child = BinaryTreeNode(
            node_type.put(x), self.get_child_ypos(),
            *self.get_l_xrange(), self.prop * self.small_prop)
        if self.show_branch:
            self.set_l_branch()
        return self.l_child

    def set_r(self, x, node_type):
        self.r_child = BinaryTreeNode(
            node_type.put(x), self.get_child_ypos(),
            *self.get_r_xrange(), self.prop * self.small_prop)
        if self.show_branch:
            self.set_r_branch()
        return self.r_child

    def shift_y_tree(self, vec=0.5):
        self.shift(vec*UP)
        if self.l_child is not None:
            self.l_child.shift_y_tree(vec)
        if self.r_child is not None:
            self.r_child.shift_y_tree(vec)


    def anim_shift_y_tree(self, vec=0.5):
        return AnimationGroup(
            self.animate.shift(vec*UP),
            self.l_child.anim_shift_y_tree(vec) if self.l_child is not None else AnimationGroup(),
            self.r_child.anim_shift_y_tree(vec) if self.r_child is not None else AnimationGroup()
        )

    def move_node(self, left, right, y_pos, prop):
        if self.submobjects.__len__() > 1:
            self.remove(self.submobjects[1])
        self.left = left
        self.right = right
        self.submobjects[0].scale(prop/self.prop)
        self.prop = prop
        mid = self.get_x_pos()
        self.move_to(y_pos * UP + mid * RIGHT)

    def move_tree(self, left, right, y_pos, prop):
        if self.submobjects.__len__() > 1:
            self.remove(self.submobjects[1])
        self.left = left
        self.right = right
        self.submobjects[0].scale(prop/self.prop)
        self.prop = prop
        mid = self.get_x_pos()
        self.submobjects[0].move_to(y_pos * UP + mid * RIGHT)

        print(self.get_y())
        if self.l_child is not None:
            self.l_child.move_tree(left, mid, y_pos - 1.2*prop, self.prop * self.small_prop)
        if self.r_child is not None:
            self.r_child.move_tree(mid, right, y_pos - 1.2*prop, self.prop * self.small_prop)

    def anim_move_tree(self, left, right, y_pos, prop):
        mid = (left + right) / 2.0
        self.left = left
        self.right = right
        return AnimationGroup(
            self.animate.move_node(left, right, y_pos, prop),
            self.l_child.anim_move_tree(left, mid, y_pos - 1.2 * prop, prop * self.small_prop)
            if self.l_child is not None else AnimationGroup(),
            self.r_child.anim_move_tree(mid, right, y_pos - 1.2 * prop, prop * self.small_prop)
            if self.r_child is not None else AnimationGroup()
        )

    def anim_move_to_parent(self, isl=True):
        if isl:
            return self.anim_move_tree(
                self.left, 2 * self.right - self.left,
                self.get_parent_ypos(), self.prop/self.small_prop)
        else:
            return self.anim_move_tree(
                2*self.left - self.right, self.right,
                self.get_parent_ypos(), self.prop / self.small_prop)

    def anim_move_to_child(self, isl=True):
        if isl:
            return self.anim_move_tree(
                self.left, self.get_x_pos(),
                self.get_child_ypos(), self.prop*self.small_prop)
        else:
            return self.anim_move_tree(
                self.get_x_pos(), self.right,
                self.get_child_ypos(), self.prop * self.small_prop)

    def anim_move_to_bro(self, isl=True):
        if isl:
            return self.anim_move_tree(
                self.right, 2 * self.right - self.left,
                self.get_real_y(), self.prop)
        else:
            return self.anim_move_tree(
                self.left, 2 * self.left - self.right,
                self.get_real_y(), self.prop)

    def anim_fade_out_tree(self):
        return AnimationGroup(
            FadeOut(self),
            self.l_child.anim_fade_out_tree() if self.l_child is not None else AnimationGroup(),
            self.r_child.anim_fade_out_tree() if self.r_child is not None else AnimationGroup()
        )

# 以下方法用于生长枝条
    def get_real_center(self):
        return self.submobjects[0].get_center()

    def get_real_x(self):
        return self.submobjects[0].get_x()

    def get_real_y(self):
        return self.submobjects[0].get_y()

    def anim_set_l_branch(self):
        if self.l_child is not None:
            t = Line(self.l_child.get_real_center(), self.get_real_center(), buff=0.5*self.prop)
            self.l_child.add(t)
            return Create(t)

    def anim_set_r_branch(self):
        if self.r_child is not None:
            t = Line(self.r_child.get_real_center(), self.get_real_center(), buff=0.5*self.prop)
            self.r_child.add(t)
            return Create(t)

    def set_l_branch(self):
        if self.l_child is not None:
            self.l_child.add(Line(self.l_child.get_real_center(), self.get_real_center(), buff=0.5*self.prop))

    def set_r_branch(self):
        if self.r_child is not None:
            self.r_child.add(Line(self.r_child.get_real_center(), self.get_real_center(), buff=0.5*self.prop))

    def set_tree_branch(self):
        if self.l_child is not None:
            self.set_l_branch()
            self.l_child.set_tree_branch()

        if self.r_child is not None:
            self.set_r_branch()
            self.r_child.set_tree_branch()

    def anim_set_tree_branch(self):
        it = list()
        if self.l_child is not None:
            it.append(self.anim_set_l_branch())
            ret = self.l_child.anim_set_tree_branch()
            for cur in ret:
                it.append(cur)
        if self.r_child is not None:
            it.append(self.anim_set_r_branch())
            ret = self.r_child.anim_set_tree_branch()
            for cur in ret:
                it.append(cur)

        return it

    def remove_child(self, p):
        if p is not None:
            t = p.l_child if p.l_child is not None else p.r_child
            if p == self.l_child:
                self.l_child = t
            if p == self.r_child:
                self.r_child = t

    def is_leaf(self):
        return self.l_child is None and self.r_child is None

    def build(self, node_type, left, right, array: list):
        mid = (left + right) >> 1
        if mid - 1 >= left:
            self.set_l(array[(mid - 1 + left) >> 1], node_type)
            self.l_child.build(node_type, left, mid - 1, array)
        if mid + 1 <= right:
            self.set_r(array[(mid + 1 + right) >> 1], node_type)
            self.r_child.build(node_type, mid + 1, right, array)

    def change_node_color(self, _color):
        self.submobjects[0][1].color = _color

    def swap_node_font_color(self):
        a = str(self.submobjects[0][0].color)
        b = str(self.submobjects[0][1].color)
        self.submobjects[0][1].color = a
        self.submobjects[0][0].color = b

    def min(self):
        p = self
        while p.l_child is not None:
            p = p.l_child
        return p

    def max(self):
        p = self
        while p.r_child is not None:
            p = p.r_child
        return p

    def nxt(self):
        if self.r_child is not None:
            p = self.r_child
            return p.min()

    def pre(self):
        if self.l_child is not None:
            p = self.l_child
            return p.max()


