from manim import *


class VisualMatrix(Scene):
    ma = []
    ma1 = []
    mo = 0
    w = 3
    h = 4
    a=2
    b=3
    def construct(self):
        self.ma = [[0 for i in range(self.w)] for i in range(self.h)]
        self.ma1 = [[1 for i in range(self.a)] for i in range(self.b)]
        self.mo = Matrix(self.ma)
        self.mo1=Matrix(self.ma1)
        self.play(Create(self.mo))
        self.change(1,1,8)
        self.swap(0,0,1,1)
        self.transpose()
        self.allchange()
        self.wait(4)
        return None

    def change(self,x,y,v):
        self.ma[x][y] = v
        it = self.mo.get_columns()[x][y]
        self.play(Transform(it, self.mo.element_to_mobject(v).move_to(it.get_x() * RIGHT + it.get_y() * UP)))

    def swap(self,m1,n1,m2,n2):
        it1 = self.mo.get_columns()[m1][n1]
        it2 = self.mo.get_columns()[m2][n2]
        it1, it2 = it2, it1
        self.play(CyclicReplace(it1, it2))
        self.ma[m1][n1],self.ma[m2][n2] = self.ma[m2][n2],self.ma[m1][n1]

    def transpose(self):
        self.ma = [[self.ma[j][i] for j in range(0, self.h)] for i in range(0, self.w)]
        self.play(Transform(self.mo, Matrix(self.ma)))

    def allchange(self):
        # self.clear()
        self.play(Transform(self.mo, Matrix(self.ma1)))







