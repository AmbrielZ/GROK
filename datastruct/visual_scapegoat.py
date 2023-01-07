from visual_bst import *

class ScapegoatTreeOrderMap(binarySearchTreeOrderMap):
    def ini(self, datastruct):
        super().ini(datastruct)
        self.set(9, self.rebuild_ini)

    def rebuild_ini(self, subtype, datas: list):
        if subtype == 1:
            self.datastruct.rebuild(*self.datastruct.find_target(datas))

class ScapegoatTree(BinarySearchTree):
    datatype = ScapegoatTreeOrderMap
    # def construct(self):
    #     self._set()
    #     self.insert(10);
    #     self.insert(12);
    #     self.insert(99);
    #     self.insert(111);
    #     self.rebuild(self.root.r_child, self.real_root.right, 1)
    #     self.insert(5);
    #     self.insert(77);
    #     self.erase(12);
    #     self.erase(111);
    #     self.erase(99);
    def find_target(self, s:str):
        p = self.root
        rp = self.real_root

        for ch in s:
            if ch == '0':
                p = p.l_child
                rp = rp.left
            else:
                p = p.r_child
                rp = rp.right
        return [p, rp, s.__len__()]

    def create_tree(self, r):
        q = list()
        q.append(r)
        anim_q = []
        now = 1
        while q.__len__() > 0:
            p = q.pop(0)
            anim_q.append(p)
            if p.l_child is not None:
                q.append(p.l_child)
            if p.r_child is not None:
                q.append(p.r_child)
            now -= 1
            if now == 0:
                now = q.__len__()
                self.play(*[Create(cur) for cur in anim_q])
                anim_q.clear()

    def rebuild(self, r, rr, cur_level):
        self.play(r.anim_fade_out_tree())
        target_arr = []

        rr.get_array(target_arr)
        self.inorder_adjust(rr,cur_level,-1)

        rr.val = target_arr[(target_arr.__len__() - 1) >> 1]
        right = target_arr.__len__() - 1
        r.change(target_arr[right >> 1], self.node_type)
        rr.build(0, right, target_arr)
        r.build(self.node_type, 0, right, target_arr)
        self.create_tree(r)
        self.inorder_set_parent(r)
        self.inorder_adjust(rr, cur_level, 1)

        erase_list = []
        for i in range(0,self.level_map.__len__()):
            if self.level_map[i] == 0:
                erase_list.append(i)

        for cur in erase_list:
            self.level_map.pop(cur)

        self.play(self.root.anim_shift_y_tree(-0.5*erase_list.__len__()))


