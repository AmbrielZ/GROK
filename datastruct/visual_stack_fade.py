from visual_arr import *

class stackOrderMap(visualArrOrderMap):
    def change_ini(self, subtype, datas: list):
        if subtype == 1:
            self.datastruct.change(-1, datas[1])

class VisualStack(VisualArr):
    inscence = 7
    tracker = None
    datatype = stackOrderMap

    def push(self, x):
        if self.tracker is None:
            self.set_tracker()
        n = self.objs_arr.__len__()

        if n < self.inscence:
            super().push(x)
        else:
            m = self.inscence - 1
            start = ((m + 1) >> 1) * LEFT
            self.row_play(n - m, n, start, RIGHT * ((m + 1.0) / m if m & 1 else 1))
            outobj = self.objs_arr[n - self.inscence]
            self.play(
                outobj.animate.move_to(((m + 3) >> 1) * LEFT),
                AnimationGroup(
                    *[
                        MoveToTarget(self.objs_arr[i])
                        for i in range(n - m, n)
                    ]
                )
            )
            self.play(FadeOut(outobj))
            self.objs_arr.append(self.node_type.put(x).move_to(start))
            self.play(Create(self.objs_arr[n]))

        if self.tracker != 0:
            self.update_tracker(n)

    def pop(self):
        n = self.objs_arr.__len__() - 1

        if self.tracker != 0:
            self.tracker[0].clear_updaters()

        if n <= self.inscence:
            super().pop()
            if self.tracker != 0:
                self.play(FadeOut(self.tracker, run_time=0.5))
                if n > 0:
                    self.tracker[0].add_updater(lambda w: w.next_to(self.objs_arr[n - 1], 0.5 * UP))
                    self.play(FadeIn(self.tracker, run_time=0.5))
        else:
            self.play(FadeOut(self.objs_arr[n]))
            self.objs_arr.remove(self.objs_arr[n])
            self.play(FadeIn(self.objs_arr[n - self.inscence]))
            m = self.inscence - 1
            start = ((m + 1) >> 1) * LEFT
            self.row_play(n - m - 1, n, start, RIGHT * ((m + 1.0) / m if m & 1 else 1))
            self.play(
                AnimationGroup(
                    *[
                        MoveToTarget(self.objs_arr[i])
                        for i in range(n - m - 1, n)
                    ]
                )
            )
            if self.tracker != 0:
                self.tracker[0].add_updater(lambda w: w.next_to(self.objs_arr[n - 1], 0.5 * UP))

    def set_tracker(self):
        pointer = Vector(DOWN * 0.5, color=self.node_type.font_c)
        tracker_label = Tex("top", font_size=50, color=self.node_type.node_c).add_updater(lambda w: w.next_to(pointer, 0.5 * UP))
        self.tracker = VGroup(pointer, tracker_label)

    def update_tracker(self, n):
        if n > 0:
            self.play(FadeOut(self.tracker, run_time=0.5))
            self.tracker[0].clear_updaters()

        self.tracker[0].\
            add_updater(lambda w: w.next_to(self.objs_arr[n], 0.5 * UP))
        self.play(FadeIn(self.tracker, run_time=0.5))
