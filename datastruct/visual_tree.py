from manim import *
import Node


class RealBinaryTreeNode:
    def __init__(self, x, l=None, r=None, p=None):
        self.val = x
        self.left = l
        self.right = r
        self.parent = p
        self.size = 1 + (l.size if l is not None else 0) + (r.size if r is not None else 0)

    def remove(self, x):
        if self.left is not None:
            if self.left.val == x:
                self.left = None
        if self.right is not None:
            if self.right.val == x:
                self.right = None

    def is_leaf(self):
        return self.left is None and self.right is None

    def build(self, left, right, array: list):
        mid = (left + right) >> 1
        if mid - 1 >= left:
            self.left = RealBinaryTreeNode(array[(mid - 1 + left) >> 1])
            self.left.parent = self
            self.left.build(left, mid - 1, array)
        if mid + 1 <= right:
            self.right = RealBinaryTreeNode(array[(mid + 1 + right) >> 1])
            self.right.parent = self
            self.right.build(mid + 1, right, array)

    def get_array(self, array: list):
        if self.left is not None:
            self.left.get_array(array)
        array.append(self.val)
        if self.right is not None:
            self.right.get_array(array)

    def set_child(self, q, isleft):
        if isleft:
            if self.left is not None:
                self.size -= self.left.size
            self.left = q
        else:
            if self.right is not None:
                self.size -= self.right.size
            self.right = q
        if q is not None:
            self.size += q.size

    def delete_child(self, q):
        if q is not None:
            t = q.left if q.left is not None else q.right
            if q == self.left:
                self.left = t
                q.parent = None
            elif q == self.right:
                self.right = t
                q.parent = None

    def min(self):
        p = self
        while p.left is not None:
            p = p.left
        return p

    def max(self):
        p = self
        while p.right is not None:
            p = p.right
        return p

    def nxt(self):
        if self.right is not None:
            p = self.right
            return p.min()
        else:
            p = self
            while p.parent is not None and p != p.parent.left:
                p = p.parent
            return p.parent

    def pre(self):
        if self.left is not None:
            p = self.left
            return p.max()
        else:
            p = self
            while p.parent is not None and p != p.parent.right:
                p = p.parent
            return p.parent


    def is_left_child(self):
        return self.parent is not None and self == self.parent.left

def inorder_print(p:RealBinaryTreeNode):
    if p.left is not None:
        inorder_print(p.left)
    print(p.val)
    if p.right is not None:
        inorder_print(p.right)


class VisualTree(Scene):
    objs_level = {}
    showLabel = 0
    node_type = Node.Node(node_type="RoundedSquare")
    root = None
    real_root = None

    def construct(self):
        pass



