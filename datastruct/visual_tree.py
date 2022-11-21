from manim import *
import Node


class VisualTree(Scene):
    objs_level = {}
    showLabel = 0
    node_type = Node.Node(node_type="RoundedSquare")
    root = None

    def construct(self):
        self.root = Node.TreeNode(self.node_type.put(10))

        self.play(Create(self.root))
        self.play(self.root.animate.shift(UP))

        p = self.root

        self.play(p.insert(5, self.node_type))
        self.wait(2)
        self.play(p.insert(15, self.node_type))
        self.wait(2)
        self.play(p.child[0].insert(45, self.node_type))
        self.play(p.animate_shift_tree())

        self.wait(5)


