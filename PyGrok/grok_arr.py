from PyGrokbase import *


class arr_test:
    def __init__(self):
        self._hrm = msg(head())
        self.arr = list()
        self._hrm.sendto(act(1, 0).push("vector"))

    def append(self, x):
        self.arr.append(x)
        self._hrm.sendto(act(3, 1).push(x))

    def __del__(self):
        self._hrm.sendto(act(-1, 0))


if __name__ == '__main__':
    arr = arr_test()
    arr.append(10)
    arr.append(12)
