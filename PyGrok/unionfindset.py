from PyGrokbase import *


class unionfindset:
    def __init__(self, _n):
        self.parent = list(range(_n))
        self.size = list()
        self.size = [1] * _n
        self._hrm = msg(head())
        self.n = _n
        self.setcount = _n
        self._hrm.sendto(act(1, 4).push("unionfindset").push(_n))

    def __del__(self):
        self._hrm.sendto(act(-1, 0))

    def findset(self, x):
        father = self.parent[x]
        if self.parent[x] == x:
            return x
        else:
            self.parent[x] = self.findset(self.parent[x])
            return self.parent[x]

    def unite(self, x, y):
        x = self.findset(x)
        y = self.findset(y)
        if x == y:
            return 0
        if self.size[x] < self.size[y]:
            t = x
            x = y
            y = t
        self.parent[y] = x
        self.size[x] += self.size[y]
        self.setcount -= 1
        self._hrm.sendto(act(3, 1).push(x).push(y))
        return 1

    def connected(self, x, y):
        x = self.findset(x)
        y = self.findset(y)
        return x == y

if __name__ == '__main__':
    self = unionfindset(10)
    self.unite(5, 6)
    self.unite(7, 9)
    self.unite(7, 8)
    self.unite(0, 9)
    self.unite(0, 5)
    self.unite(6, 1)
    self.unite(9, 2)
    self.unite(3, 4)
    self.unite(3, 8)
    print(self.findset(0))




