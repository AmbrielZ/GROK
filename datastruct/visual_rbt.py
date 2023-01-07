from visual_bst import *

class RedBlackTree(BinarySearchTree):
    is_black = {}
    color_of_r = Node.PK
    color_of_b = "#3FFF3F"


    def __is_black(self, real_p):
        return self.is_black[real_p] == True

    def __is_red(self, real_p):
        return self.is_black[real_p] == False

    def real_root_judge(self, real_p):
        if real_p.parent is None:
            self.real_root = real_p
        return real_p == self.real_root

    def insert(self, x):
        [p, real_p] = super().insert(x)
        self.balance_after_insert(p, real_p)

    def balance_after_insert(self, p:Node.BinaryTreeNode,real_p:RealBinaryTreeNode):
        self.is_black[real_p] = False

        self.set_node_color(p, real_p, self.real_root_judge(real_p))
        while real_p != self.real_root and self.__is_red(real_p.parent):
            if real_p.parent == real_p.parent.parent.left:

                real_q = real_p.parent.parent.right

                if real_q is not None and self.__is_red(real_q):
                    q = self.parent_map[self.parent_map[p]].r_child
                    real_p = real_p.parent
                    p = self.parent_map[p]
                    self.set_node_color(p, real_p, True)

                    real_p = real_p.parent
                    p = self.parent_map[p]
                    self.set_node_color(p, real_p, self.real_root_judge(real_p))
                    self.set_node_color(q, real_q, True)
                else:
                    if real_p == real_p.parent.right:
                        real_p = real_p.parent
                        p = self.parent_map[p]
                        self.lef_rotate(p, real_p)

                    real_p = real_p.parent
                    p = self.parent_map[p]
                    self.set_node_color(p, real_p, True)

                    real_p = real_p.parent
                    p = self.parent_map[p]
                    self.set_node_color(p, real_p, False)

                    self.rig_rotate(p, real_p)
                    break
            else:
                real_q = real_p.parent.parent.left

                if real_q is not None and self.__is_red(real_q):
                    q = self.parent_map[self.parent_map[p]].l_child
                    real_p = real_p.parent
                    p = self.parent_map[p]
                    self.set_node_color(p, real_p, True)

                    real_p = real_p.parent
                    p = self.parent_map[p]
                    self.set_node_color(p, real_p, self.real_root_judge(real_p))
                    self.set_node_color(q, real_q, True)
                else:
                    if real_p == real_p.parent.left:
                        real_p = real_p.parent
                        p = self.parent_map[p]
                        self.rig_rotate(p, real_p)

                    real_p = real_p.parent
                    p = self.parent_map[p]
                    self.set_node_color(p, real_p, True)

                    real_p = real_p.parent
                    p = self.parent_map[p]
                    self.set_node_color(p, real_p, False)

                    self.lef_rotate(p, real_p)
                    break

    def set_node_color(self, p:Node.BinaryTreeNode, real_p:RealBinaryTreeNode, flag:bool):
        #flag为1则将节点转为黑=PK， flag为0转为红=WHITE
        if self.__is_black(real_p) ^ flag:
            self.play(p.animate.change_node_color(self.color_of_b if flag else self.color_of_r))
            self.is_black[real_p] = flag

    def erase(self, x):
        ls = self.erase_find(x)
        _z = ls[0]
        __z = ls[1]
        flag = True

        __y = __z if __z.left is None or __z.right is None else __z.nxt()
        _y = _z if _z.l_child is None or _z.r_child is None else _z.nxt()

        __x = __y.left if __y.left is not None else __y.right
        _x = _y.l_child if _y.l_child is not None else _y.r_child

        __w = None
        _w = None

        if __x is not None:
            __x.parent = __y.parent
            self.take_of_parent(self.parent_map[_x], _x)
            flag = False
        if flag:
            self.play(_y.anim_fade_out_tree())
            if __y != self.real_root:
                self.parent_map[_y].remove_child(_y)

        if __y == self.real_root:
            self.real_root = __x
            self.root = _x
        elif __y.is_left_child():
            __y.parent.left = __x
            self.parent_map[_y].l_child = _x

            if __y != self.real_root:
                __w = __y.parent.right
                _w = self.parent_map[_y].r_child
            else:
                self.real_root = __x
                self.root = _x
        else:
            __y.parent.right = __x
            self.parent_map[_y].r_child = _x

            __w = __y.parent.left
            _w = self.parent_map[_y].l_child

        __removed_black = self.is_black[__y]

        if __y != __z:
            if __z != self.real_root:
                __y.parent = __z.parent

                if __z.is_left_child():
                    __y.parent.left = __y
                else:
                    __y.parent.right = __y

                __y.left = __z.left
                if __y.left is not None:
                    __y.left.parent = __y

                __y.right = __z.right
                if __y.right is not None:
                    __y.right.parent = __y

                self.is_black[__y] = self.is_black[__z]
                self.play(_z.animate.change(__y.val, self.node_type))
                if self.real_root == __z:
                    self.real_root = __y
            else:
                __z.val = __y.val
                __y.parent.delete_child(__y)
                __y = __z
                self.parent_map[_y].remove_child(_y)
                self.play(_z.animate.change(__y.val, self.node_type))


        self.parent_map.pop(_y)

        if __removed_black and self.real_root is not None:
            if __x is not None:
                self.set_node_color(_x, __x, True)
            else:
                while True:
                    if not __w.is_left_child():
                        if self.__is_red(__w):
                            self.set_node_color(_w, __w, True)
                            self.set_node_color(self.parent_map[_w], __w.parent, False)
                            self.lef_rotate(self.parent_map[_w], __w.parent)

                            if self.real_root == __w.left:
                                self.real_root = __w
                                self.root = _w

                            __w = __w.left.right
                            _w = _w.l_child.r_child
                        if ((__w.left is None or self.is_black[__w.left]) and
                                (__w.right is None or self.is_black[__w.right])):
                            self.set_node_color(_w, __w, False)
                            __x = __w.parent
                            _x = self.parent_map[_w]
                            if __x == self.real_root or self.__is_red(__x):
                                self.set_node_color(_x, __x, True)
                                break
                            if __x.is_left_child():
                                __w = __x.parent.right
                                _w = self.parent_map[_x].r_child
                            else:
                                __w = __x.parent.left
                                _w = self.parent_map[_x].l_child
                        else:
                            if __w.right is None or self.__is_black(__w.right):
                                self.set_node_color(_w.l_child, __w.left, True)
                                self.set_node_color(_w, __w, False)
                                self.rig_rotate(_w, __w)
                                __w = __w.parent
                                _w = self.parent_map[_w]
                            self.set_node_color(_w, __w, self.is_black[__w.parent])
                            self.set_node_color(self.parent_map[_w], __w.parent, True)
                            self.set_node_color(_w.r_child, __w.right, True)
                            self.lef_rotate(self.parent_map[_w], __w.parent)
                            break
                    else:
                        if self.__is_red(__w):
                            self.set_node_color(_w, __w, True)
                            self.set_node_color(self.parent_map[_w], __w.parent, False)
                            self.rig_rotate(self.parent_map[_w], __w.parent)

                            if self.real_root == __w.right:
                                self.real_root = __w
                                self.root = _w

                            __w = __w.right.left
                            _w = _w.r_child.l_child
                        if ((__w.left is None or self.__is_black(__w.left)) and
                                (__w.right is None or self.__is_black(__w.right))):
                            self.set_node_color(_w, __w, False)
                            __x = __w.parent
                            _x = self.parent_map[_w]
                            if __x == self.real_root or self.__is_red(__x):
                                self.set_node_color(_x, __x, True)
                                break
                            if __x.is_left_child():
                                __w = __x.parent.right
                                _w = self.parent_map[_x].r_child
                            else:
                                __w = __x.parent.left
                                _w = self.parent_map[_x].l_child
                        else:
                            if __w.left is None or self.__is_black(__w.left):
                                self.set_node_color(_w.r_child, __w.right, True)
                                self.set_node_color(_w, __w, False)
                                self.lef_rotate(_w, __w)
                                __w = __w.parent
                                _w = self.parent_map[_w]

                            self.set_node_color(_w, __w, self.is_black[__w.parent])
                            self.set_node_color(self.parent_map[_w], __w.parent, True)
                            self.set_node_color(_w.l_child, __w.left, True)
                            self.rig_rotate(self.parent_map[_w], __w.parent)
                            break
