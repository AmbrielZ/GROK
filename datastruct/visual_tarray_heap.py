from visual_tarray import *
from visual_arr_heap import *


class VisualTreeHeap(VisualTarray, VisualArrHeap):
    def construct(self):
        super().init([10, 5, 6, 7])

    def push(self, x):
        super().push(x)
        self.arr.append(x)
        self.heapify(self.objs_arr.__len__() - 1)