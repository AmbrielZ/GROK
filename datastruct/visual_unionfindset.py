from manim import *
import Node

class unionFindSetOrderMap(Node.orderMap):
    def ini(self, datastruct):
        self.datastruct = datastruct
        self.set(0, self.set_ini)
        self.set(1, self.init_ini)
        self.set(3,self.unite_ini)

    def init_ini(self, subtype, datas: list):
        if subtype == 4:
            self.datastruct.init(int(datas[0]))

    def unite_ini(self, subtype, datas: list):
        if subtype == 1:
            self.datastruct.unite(int(datas[0]), int(datas[1]))

    def set_ini(self, subtype, datas: list):
        pass

class UnionFindSet(Scene):
    parent = []
    size = []
    obj_graph = 0
    reader = Node.reader()
    datatype = unionFindSetOrderMap

    def _set(self):
        order_map = self.datatype()
        order_map.ini(self)
        self.reader.__int__(order_map=order_map)

    def construct(self):
        self._set()
        self.reader.read_from()
        self.wait()

    def init(self, n):
        self.parent = [cur for cur in range(n)]
        self.size = [1 for _ in range(n)]
        self.obj_graph = Graph(self.parent, [], labels=True, layout="circular", layout_scale=3)
        self.play(FadeIn(self.obj_graph))

    def init_by_arr(self, pt, sz):
        n = pt.__len__()
        self.parent = [cur for cur in range(n)]
        self.size = [cur for cur in sz]

        self.obj_graph = Graph(self.parent, [], labels=True, layout="circular", layout_scale=3)
        for i in range(n):
            if i != pt[i]:
                self.obj_graph.add_edges((i, pt[i]))
        self.play(FadeIn(self.obj_graph))

    def link(self, x, y):
        if x != y:
            self.play(self.obj_graph.animate.add_edges((x, y)))

    def unlink(self, x, y):
        if x != y:
            self.play(self.obj_graph.animate.remove_edges((x, y)))

    def findset(self, x):
        if self.parent[x] != x:
            tmp = int(self.parent[x])
            self.parent[x] = self.findset(self.parent[x])
            if tmp != self.parent[x]:
                self.unlink(x, tmp)
                self.link(x, self.parent[x])

        return self.parent[x]

    def unite(self, x, y):
        x = self.findset(x)
        y = self.findset(y)
        if x == y:
            return 0
        if self.size[x] < self.size[y]:
            x, y = y, x

        if self.obj_graph.edges.get((y, self.parent[y])):
            self.unlink(y, self.parent[y])
        self.parent[y] = x
        self.link(y, x)
        self.size[x] += self.size[y]
        return 1
