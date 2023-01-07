from PyGrokbase import *


class vector:
    def __init__(self):
        self.num = str()
        self._x = -1
        self._y = None
        self._hrm = msg(head())
        self.vector = list()
        self._hrm.sendto(act(1, 0).push("vector"))

    def push(self, x):
        self._check()
        self.vector.append(x)
        self._hrm.sendto(act(3, 1).push(x))

    def _check(self):
        if self._x >= 0:
            t = self.vector[self._x]
            if t != self._y:
                self._hrm.sendto(act(2, 1).push(self._x).push(t))
            _x = -1

    def empty(self):
        return self.vector.__len__() == 0

    def pop(self):
        self._check()
        if self.empty():
            return None
        else:
            self.vector.pop()
            self._hrm.sendto(act(4, 0))

    def top(self):
        self._check()
        if self.empty():
            return None
        else:
            return self.vector[-1]

    def insert(self, index, x, n=1):
        self._check()
        t = index
        if isinstance(x, list):
            for _i in range(x.__len__()):
                self.vector.insert(index, x[_i])
                index += 1
                self.num += ' ' + str(x[_i])
            self._hrm.sendto(act(5, 2).push(t).push(self.num))
        elif isinstance(x, vector):
            for _i in range(x.__len__()):
                self.vector.insert(index, x[_i])
                index += 1
                self.num += ' ' + str(x[_i])
            self._hrm.sendto(act(5, 2).push(t).push(self.num))
        else:
            if n == 1:
                self.vector.insert(index, x)
                self._hrm.sendto(act(5, 1).push(t).push(x))
            else:
                for _i in range(n):
                    self.vector.insert(index, x)
                self._hrm.sendto(act(5, 3).push(t).push(n).push(x))

    def swap(self, x, p):
        self._check()
        t = self.vector[x]
        self.vector[x] = self.vector[p]
        self.vector[p] = t
        self._hrm.sendto(act(7, 1).push(x).push(p))

    def erase(self, index, n=1):
        self._check()
        if n == 1:
            self.vector.pop(index)
            self._hrm.sendto(act(6, 1).push(index))
        else:
            for _i in range(n - index + 1):
                self.vector.pop(index)
            self._hrm.sendto(act(6, 2).push(index).push(n))

    def clear(self):
        self._check()
        self.vector.clear()
        self._hrm.sendto(act(8, 0))

    def __len__(self):
        return len(self.vector)

    def __getitem__(self, index):
        self._check()
        return self.vector[index]

    def __setitem__(self, index, newitem):
        self._check()
        self.vector[index] = newitem
        _x = int(index)
        _y = newitem
        return self.vector[index]

    def __del__(self):
        self._check()
        self._hrm.sendto(act(-1, 0))


if __name__ == '__main__':
    a = vector()
    a.push(10)

    c = vector()
    c.push(20)
    c.push(30)
    a.insert(0, c)
    a.insert(0, 3, 4)
    a.swap(3, 4)
    a.erase(3, 4)
    a[1] = 99
    a.erase(0)
    for i in range(a.__len__()):
        print(a[i])
