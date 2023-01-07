from PyGrokbase import *
from heapq import *


class heap:
    def __init__(self, arr=None):
        self._hrm = msg(head())
        self.heap = list()
        self._n = 0
        if arr is None:
            arr = []
        if len(arr) == 0:
            self._hrm.sendto(act(1, 0).push("heap"))
        else:
            self._hrm.sendto(act(1, 0).push("heap"))
            self._n = len(arr)
            for _i in range(self._n):
                self.push(arr[_i])

    def push(self, x):
        heappush(self.heap, x)
        self._n += 1
        self._hrm.sendto(act(3, 1).push(x))

    def pop(self):
        heappop(self.heap)
        self._n -= 1
        self._hrm.sendto(act(4, 0))

    def front(self):
        if self.empty():
            print("Heap is empty")
        return self.heap[0]

    def empty(self):
        return self._n == 0

    def __del__(self):
        self._hrm.sendto(act(-1, 0))

    def __str__(self):
        return str(self.heap)


if __name__ == '__main__':
    arr = [1, 4, 0, 10, 20, 99, 20, 7]
    h1 = heap(arr)
    print(h1)
