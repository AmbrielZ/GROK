from visual_arr import *


class VisualArrHeap(VisualArr):
    arr = []

    def construct(self):
        self.init([10, 5, 7, 20, 14, 20])

    def init(self, arr: list):
        for cur in arr:
            self.push(cur)

    def push(self, x):
        super().push(x)
        self.arr.append(x)
        self.heapify(self.objs_arr.__len__() - 1)

    def heapify(self, j):
        key = self.arr[j]
        while j > 0 and self.arr[self.get_f(j)] > key:
            k = self.get_f(j)
            self.arr[j] = self.arr[k]
            self.swap(j, k)
            j = k
        self.arr[j] = key

    def pop(self):
        n = self.objs_arr.__len__()
        self.swap(0, n - 1)
        self.play(FadeOut(self.objs_arr[n-1]))
        self.objs_arr.remove(self.objs_arr[n-1])

        self.arr[0],  self.arr[n - 1] = self.arr[n-1], self.arr[0]
        self.arr.pop(n - 1)
        key = self.arr[0]
        i = 0
        j = 0
        n -= 1
        while j < n:
            if j + 1 < n and self.arr[j] > self.arr[j + 1]:
                j += 1
            if key > self.arr[j]:
                self.arr[i] = self.arr[j]
                self.swap(i, j)
                i = j
            else:
                break
            j = (j << 1 | 1)
        self.arr[i] = key


    def get_f(self, i) -> int:
        return (i - 1) >> 1