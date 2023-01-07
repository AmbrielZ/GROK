from visual_arr import *




class VisualTarray(VisualArr):
    def get_level(self, n) -> int:
        count = 0
        tmp = n
        while tmp > 0:
            tmp >>= 1
            count += 1
        return count

    def push(self, x):
        n = self.objs_arr.__len__()

        self.objs_arr.append(
            self.node_type.put(x).move_to(self.arrange(n))
        )
        self.play(Create(self.objs_arr[n]))

    def pop(self):
        n = self.objs_arr.__len__()
        if n == 0:
            return None
        n -= 1

        self.play(FadeOut(self.objs_arr[n]))
        self.objs_arr.remove(self.objs_arr[n])

        if n == 0:
            return None

        self.arrange(n, 0)

    def arrange(self, m, t = 1):
        levels = self.get_level(m + t) - 1
        start = 0
        y_gap = (1 << levels)
        now = 0

        while ((2 << now) - 1) < m:

            self.row_play((1 << now) - 1, (2 << now) - 1, start * LEFT * 0.5,
                          0.5 * (y_gap << 1) * RIGHT,
                          0.5 * levels * UP + now * DOWN)
            now += 1
            y_gap >>= 1
            start += y_gap

        tmp = start * LEFT * 0.5
        if m > 0:
            self.row_play((1 << now) - 1, m,
                          tmp, 0.5 * (y_gap << 1) * RIGHT,
                          0.5 * levels * UP + now * DOWN)
            now += 1
            self.play(
                AnimationGroup(
                    *[
                        MoveToTarget(cur)
                        for cur in self.objs_arr
                    ]
                )
            )

        if m == ((1 << now) - 1):
            now += 1
            start += (y_gap >> 1)
            tmp = 0.5 * start * LEFT

        return tmp + 0.5 * levels * UP + (now - 1) * DOWN
