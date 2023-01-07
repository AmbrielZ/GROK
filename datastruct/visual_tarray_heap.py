from visual_tarray import *
from visual_arr_heap import *

class VisualTreeHeap(VisualTarray, VisualArrHeap):

    def push(self, x):
        super().push(x)
        self.data_arr.append(x)
        self.heapify(self.objs_arr.__len__() - 1)

    def pop(self):
        VisualArrHeap.pop(self)