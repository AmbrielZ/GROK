from visual_tarray import *

class segmentTreeOrderMap(Node.orderMap):
    def ini(self, datastruct):
        self.datastruct = datastruct
        self.set(0, self.set_ini)
        self.set(1,self.init_ini)
        self.set(3,self.add_ini)

    def init_ini(self, subtype, datas: list):
        if subtype == 1:
            self.datastruct.init(int(datas[0]))
        elif subtype == 2:
            self.datastruct.set_lazy()
            self.datastruct.init(int(datas[0]))
        elif subtype == 3:
            self.datastruct.init_by_arr(datas)


    def add_ini(self, subtype, datas: list):
        if subtype == 1:
            self.datastruct.add_single(int(datas[0]), int(datas[1]))
        elif subtype == 2:
            self.datastruct.add_multiple(int(datas[0]), int(datas[1]), int(datas[2]))

    def set_ini(self, subtype, datas:list):
        pass
        # self.datastruct.node_set(datas[0], datas[1], datas[2], int(datas[3]), float(datas[4]))


class SegmentTree(VisualTarray):
    segment_tree = []
    objs_arr = []
    lazy_arr = []
    showLabel = 0
    showLazy = False
    datatype = segmentTreeOrderMap

    def init_by_arr(self, arr):
        n = arr.__len__() - 1
        self.objs_arr = [Mobject() for _ in range(0, n + 1)]
        self.segment_tree = arr
        self.lazy_arr = [0 for _ in range(0, n + 1)]
        self.init_rec(1, n >> 1, 1)

        if n > 0:
            self.init_arrange(n)


    def _set(self, font_color = Node.CYAN, node_color = Node.PK, node_size = 0.8, node_type ="Circle", label = 0):
        order_map = self.datatype()
        order_map.ini(self)
        self.reader.__int__(order_map=order_map)
        self.node_type.__init__(font_color, node_color, node_size, node_type)
        self.showLabel = label

    def set_lazy(self):
        self.showLazy = True

    def construct(self):
        self._set(node_type="Circle", node_size=0.5)
        self.reader.read_from()
        self.wait()

    def init(self, n):
        self.objs_arr = [Mobject() for _ in range(0, n+1)]
        self.segment_tree = [0 for _ in range(0, n+1)]
        self.lazy_arr = [0 for _ in range(0, n + 1)]
        self.init_rec(1, n >> 1, 1)

        if n > 0:
            self.init_arrange(n)

    def init_rec(self, left, right, i):
        self.objs_arr[i] = \
            self.node_type.put_labels(
                self.segment_tree[i], [str(0), '[' + str(left) + ',' + str(right) + ']'],
                [0.8*UP, DOWN], [0.3, 0.7]) if self.showLazy else \
            self.node_type.put_label(self.segment_tree[i], '[' + str(left) + ',' + str(right) + ']')
        if left == right:
            return None
        mid = (left + right) >> 1
        self.init_rec(left, mid, i << 1)
        self.init_rec(mid + 1, right, i << 1 | 1)

    def init_arrange(self, m):
        levels = self.get_level(m - 1) - 1
        start = 0
        y_gap = (1 << levels)
        now = 0
        prop = self.node_type.node_s * 1.5

        while ((2 << now) - 1) < m:
            self.row_init((1 << now), (2 << now), (start * LEFT * 0.5) * prop,
                          prop * (0.5 * (y_gap << 1) * RIGHT),
                          0.5 * levels * UP + now * DOWN)
            now += 1
            y_gap >>= 1
            start += y_gap

        tmp = start * LEFT * 0.5 * prop
        if m > 0:
            self.row_init((1 << now), m,
                          tmp, (0.5 * (y_gap << 1) * RIGHT) * prop,
                          0.5 * levels * UP + now * DOWN)
            now += 1
            self.play(
                AnimationGroup(
                    *[
                        FadeIn(cur)
                        for cur in self.objs_arr
                    ]
                )
            )

    def row_init(self, st, end, x_start, x_gap, y=UP + DOWN):
        if end - st <= 0:
            return None
        for i in range(st, end):
            cur = self.objs_arr[i]
            cur.move_to(y + x_start)
            x_start += x_gap

    def add_single(self, k, x):
        if 1 <= x <= self.objs_arr.__len__():
            self.add_single_rec(k, x, 1, self.objs_arr.__len__()>>1, 1)

    def add_multiple(self, k, l, r):
        if 1 <= l < r <= (self.objs_arr.__len__()>>1):
            self.add_multiple_rec(k,l,r,1,self.objs_arr.__len__()>>1,1)

    def add_single_rec(self, k, x, left, right, i):
        self.segment_tree[i] += k
        self.change(i, self.segment_tree[i])
        if left == right:
            return None
        mid = (left + right) >> 1
        if mid >= x:
            self.add_single_rec(k, x, left, mid, i << 1)
        else:
            self.add_single_rec(k, x, mid + 1, right, i << 1 | 1)

    def add_multiple_rec(self, k, l, r, left, right, i):
        if self.showLazy == True and l == left and r == right and l != r:
            self.lazy_arr[i] += k
            self.lazy_change(i, self.lazy_arr[i])
            return None
        self.segment_tree[i] += k * (r - l + 1)
        self.change(i, self.segment_tree[i])
        if left == right:
            return None
        mid = (left + right) >> 1
        if mid >= r:
            self.add_multiple_rec(k, l, r, left, mid, i << 1)
        elif mid < l:
            self.add_multiple_rec(k, l, r, mid + 1, right, i << 1 | 1)
        else:
            self.add_multiple_rec(k, l, mid, left, mid, i << 1)
            self.add_multiple_rec(k, mid + 1, r, mid + 1, right, i << 1 | 1)

    def lazy_adjust(self, left, right, i):

        k = self.lazy_arr[i]
        self.lazy_arr[i] = 0
        self.lazy_change(i, 0)

        self.segment_tree[i] += (right - left + 1) * k
        self.change(i, self.segment_tree[i])
        if left != right:
            self.lazy_arr[i << 1] += k
            self.lazy_arr[i << 1 | 1] += k
            self.play(
                self.lazy_change_anim(i << 1, self.lazy_arr[i << 1]),
                self.lazy_change_anim(i << 1 | 1, self.lazy_arr[i << 1 | 1])
            )

    def change(self, i, x):
        self.play(Transform(
            self.objs_arr[i][0][0],
            self.node_type.get_font(x).move_to(self.objs_arr[i][0].get_center())
        ))

    def lazy_change(self, i, x):
        self.play(Transform(
            self.objs_arr[i][1],
            self.node_type.get_font(x, 0.3).move_to(self.objs_arr[i][1].get_center())
        ))

    def lazy_change_anim(self, i, x):
        return Transform(
            self.objs_arr[i][1],
            self.node_type.get_font(x, 0.3).move_to(self.objs_arr[i][1].get_center())
        )


