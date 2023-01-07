from visual_tree import *

class binarySearchTreeOrderMap(Node.orderMap):
    def ini(self, datastruct):
        self.datastruct = datastruct
        self.set(0, self.set_ini)
        self.set(1, self.init_ini)
        self.set(5,self.insert_ini)
        self.set(6,self.erase_ini)

    def init_ini(self, subtype, datas: list):
        # if subtype == 3:
        #     self.datastruct.init(datas)
        pass

    def insert_ini(self, subtype, datas: list):
        if subtype == 1:
            self.datastruct.insert(int(datas[0]))

    def erase_ini(self, subtype, datas: list):
        if subtype == 1:
            self.datastruct.erase(int(datas[0]))

    def set_ini(self, subtype, datas:list):
        self.datastruct.node_set(datas[0], datas[1], datas[2], int(datas[3]), float(datas[4]))

class BinarySearchTree(Scene):
    objs_level = {}
    showLabel = 0
    level_map = dict()
    parent_map = dict()
    root = None
    real_root = None
    reader = Node.reader()
    datatype = binarySearchTreeOrderMap

    def _set(self):
        order_map = self.datatype()
        order_map.ini(self)
        self.node_type = Node.Node(node_type="Circle")
        self.reader.__int__(order_map=order_map)

    def node_set(self, node_type ="Circle", font_color = Node.CYAN, node_color = Node.PK, label = 0, node_size = 0.8):
        self.node_type.__init__(font_color=font_color, node_color=node_color, node_size=node_size, node_type=node_type)
        self.showLabel = label

    def construct(self):
        self._set()
        self.reader.read_from()
        self.wait()

    def insert(self, x):
        if self.root is None:
            self.level_map[0] = 1
            self.root = Node.BinaryTreeNode(self.node_type.put(x))
            self.real_root = RealBinaryTreeNode(x)
            self.parent_map[self.root] = None
            self.play(Create(self.root))
            return [self.root, self.real_root]

        cur_level = 0
        p = self.root
        rp = self.real_root

        while rp and rp.val != x:
            rp.size += 1
            cur_level += 1
            if rp.val > x:
                if rp.left is not None:
                    p = p.l_child
                    rp = rp.left
                else:
                    rp.left = RealBinaryTreeNode(x, p=rp)
                    if not self.level_map.get(cur_level):
                        self.play(self.root.anim_shift_y_tree())
                    self.play(Create(p.set_l(x, self.node_type)))
                    self.parent_map[p.l_child] = p
                    break
            else:
                if rp.right is not None:
                    p = p.r_child
                    rp = rp.right
                else:
                    rp.right = RealBinaryTreeNode(x, p=rp)
                    if not self.level_map.get(cur_level):
                        self.play(self.root.anim_shift_y_tree())
                    self.play(Create(p.set_r(x, self.node_type)))
                    self.parent_map[p.r_child] = p
                    break

        if self.level_map.get(cur_level):
            self.level_map[cur_level] += 1
        else:
            self.level_map[cur_level] = 1

        if x > rp.val:
            return [p.r_child, rp.right]
        else:
            return [p.l_child, rp.left]

    def erase_find(self, x) -> [Node.BinaryTreeNode, RealBinaryTreeNode]:
        cur_level = 0
        p = self.root
        rp = self.real_root
        while rp and rp.val != x:
            rp.size -= 1
            cur_level += 1
            if rp.val > x:
                p = p.l_child
                rp = rp.left
            else:
                p = p.r_child
                rp = rp.right
        return [p, rp, cur_level]

    def erase(self, x):
        [p, rp, cur_level] = self.erase_find(x)

        if rp.left is not None and rp.right is not None:
            rp.size -= 1
            cur_level += 1
            rq = rp
            q = p
            rp = rp.right
            p = p.r_child
            if rp.is_leaf():
                x = rp.val
            else:
                while rp.left is not None:
                    rp.size -= 1
                    cur_level += 1
                    rp = rp.left
                    p = p.l_child
                x = rp.val

            self.play(q.animate.change(x, self.node_type))
            rq.val = x

        if rp.left is None and rp.right is None:
            self.play(FadeOut(p))
            self.level_map[cur_level] -= 1

            if rp.parent is not None:
                rp.parent.remove(x)
                self.parent_map[p].remove_child(p)
            else:
                self.root = None
                self.real_root = None
        else:
            cur_level = self.level_order(rp, cur_level)
            # 动画效果
            self.take_of_parent(p, p.l_child if p.l_child is not None else p.r_child)
            # 实际节点
            self.real_take_of_parent(rp, rp.left if rp.left is not None else rp.right)

        if self.level_map[cur_level] == 0:
            self.level_map.pop(cur_level)
            if self.root is not None:
                self.play(self.root.anim_shift_y_tree(-0.5))



    def take_of_parent(self, parent, child):
        self.play(FadeOut(parent))
        self.play(child.anim_move_to_parent(parent.l_child == child))
        if parent.submobjects.__len__() > 1:
            t = parent.submobjects[1].copy()

            self.play(Create(t), *child.anim_set_tree_branch())
            child.add(t)
        elif not child.is_leaf():
            self.play(*child.anim_set_tree_branch())

        if self.parent_map[parent] is None:
            self.root = child
        elif self.parent_map[parent].l_child == parent:
            self.parent_map[parent].l_child = child
        else:
            self.parent_map[parent].r_child = child

        self.parent_map[child] = self.parent_map[parent]

    def real_take_of_parent(self, parent, child):
        pp = parent.parent
        if pp is not None:
            if pp.left == parent:
                pp.left = child
            else:
                pp.right = child
        else:
            self.real_root = child

    @staticmethod
    def find_min(pointer, real_pointer):
        rp = real_pointer
        p = pointer
        while rp.left is not None:
            rp = rp.left
            p = p.l_child

    def rig_rotate(self, p:Node.BinaryTreeNode, real_p:RealBinaryTreeNode):
        self.real_rig_rotate(real_p)
        self.anim_rig_rotate(p)

    def real_rig_rotate(self, real_p:RealBinaryTreeNode):
        real_q = real_p.left
        real_p.set_child(real_q.right,True)


        if real_p.left is not None:
            real_p.left.parent = real_p

        real_q.parent = real_p.parent

        if real_p.parent is not None:
            if real_p.parent.left == real_p:
                real_p.parent.set_child(real_q, True)
            else:
                real_p.parent.set_child(real_q, False)

        real_q.right = real_p
        real_p.parent = real_q

        if real_p == self.real_root:
            self.real_root = real_q

    def anim_rig_rotate(self, p:Node.BinaryTreeNode):
        q = p.l_child
        p.l_child = q.r_child

        if p.l_child is not None:
            self.parent_map[p.l_child] = p

        self.parent_map[q] = self.parent_map[p]

        r = self.parent_map[p]

        if r is not None:
            if r.l_child == p:
                r.l_child = q
            else:
                r.r_child = q
        else:
            self.root = q

        q.r_child = p
        self.parent_map[p] = q

        self.play(q.anim_move_to_parent(1))
        self.play(*q.anim_set_tree_branch())

        if q is not self.real_root and r is not None:
            if r.l_child == q:
                self.play(r.anim_set_l_branch())
            else:
                self.play(r.anim_set_r_branch())

        if p == self.root:
            self.root = q

    def lef_rotate(self, p:Node.BinaryTreeNode, real_p:RealBinaryTreeNode):
        self.real_lef_rotate(real_p)
        self.anim_lef_rotate(p)

    def real_lef_rotate(self, real_p:RealBinaryTreeNode):
        real_q = real_p.right
        real_p.right = real_q.left

        if real_p.right is not None:
            real_p.right.parent = real_p

        real_q.parent = real_p.parent

        if real_p.parent is not None:
            if real_p.parent.left == real_p:
                real_p.parent.left = real_q
            else:
                real_p.parent.right = real_q

        real_q.left = real_p
        real_p.parent = real_q

        if real_p == self.real_root:
            self.real_root = real_q

    def anim_lef_rotate(self, p:Node.BinaryTreeNode):
        q = p.r_child
        p.r_child = q.l_child


        if p.r_child is not None:
            self.parent_map[p.r_child] = p

        self.parent_map[q] = self.parent_map[p]

        r = self.parent_map[p]

        if r is not None:
            if r.l_child == p:
                r.l_child = q
            else:
                r.r_child = q
        else:
            self.root = q

        q.l_child = p
        self.parent_map[p] = q


        self.play(q.anim_move_to_parent(0))
        self.play(*q.anim_set_tree_branch())

        if q is not self.real_root and r is not None:
            if r.l_child == q:
                self.play(r.anim_set_l_branch())
            else:
                self.play(r.anim_set_r_branch())

        if p == self.root:
            self.root = q

    def change_node_color(self, p:Node.BinaryTreeNode, _color=RED):
        self.play(p.animate.change_node_color(_color))

    def inorder_set_parent(self, r):
        if r is None:
            return None
        if self.inorder_set_parent(r.l_child) is not None:
            self.parent_map[r.l_child] = r

        if self.inorder_set_parent(r.r_child) is not None:
            self.parent_map[r.r_child] = r
        return self

    def inorder_adjust(self, rr, cur_level, add = 1):
        if rr is None:
            return None
        self.inorder_adjust(rr.left, cur_level + 1, add)

        self.level_map[cur_level] += add

        self.inorder_adjust(rr.right, cur_level + 1, add)

    def level_order(self, r, y):
        if r is not None:
            q = [r]
            now = 1
            level = y
            self.level_map[level] -= 1
            while q.__len__() > 0:
                front = q.pop(0)
                now -= 1
                if front.left is not None:
                    q.append(front.left)
                if front.right is not None:
                    q.append(front.right)
                if now == 0:
                    if q.__len__() > 0:
                        now = q.__len__()
                        self.level_map[level] += now
                        level += 1
                        self.level_map[level] -= now
            return level

