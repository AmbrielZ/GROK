from PyGrokbase import *


class grok_BST:
    def __init__(self, _type="Bst"):
        self.root = None
        self._size = 0
        self._hrm = msg(head())
        self._hrm.sendto(act(1, 0).push(_type))

    def __del__(self):
        self._hrm.sendto(act(-1, 0))

    def insert(self, x):
        if self.find(x):
            return 0
        self._hrm.sendto(act(5, 1).push(x))
        p = self.root
        while p and p.val != x:
            p.size += 1
            if p.val > x:
                if p.left:
                    p = p.left
                else:
                    p.left = grok_TreeNode(x)
                    break
            else:
                if p.right:
                    p = p.right
                else:
                    p.right = grok_TreeNode(x)
                    break
        if not self.root:
            self.root = grok_TreeNode(x)
        self._size += 1
        return self._size

    def erase(self, x):
        if not self.find(x):
            return 0
        self._hrm.sendto(act(6, 1).push(x))
        p = self.root
        q = None
        while p.val != x:
            p.size -= 1
            q = p
            if p.val > x:
                p = p.left
            else:
                p = p.right
        if p.left and p.right:
            r = p
            p.size -= 1
            q = p
            p = p.left
            while p.right:
                p.size -= 1
                q = p
                p = p.right
            r.val = p.val
            x = r.val
        if p.left:
            r = p.left
        else:
            r = p.right
        if q:
            if x > q.val:
                q.right = r
            else:
                q.left = r
        else:
            self.root = r
        self._size -= 1
        return 1

    def successor(self, x):
        p = self.root
        q = None
        while p and p.val != x:
            if p.val > x:
                q = p
                p = p.left
            else:
                p = p.right
        if p and p.right:
            return self.minimu(p.right)
        else:
            return q.val

    def predessor(self, x):
        p = self.root
        q = None
        while p and p.val != x:
            if p.val < x:
                q = p
                p = p.right
            else:
                p = p.left
        if p and p.left:
            return self.maximu(p.left)
        else:
            return q.val

    def maximu(self, p):
        if not p:
            return None
        while p.right:
            p = p.right
        return p.val

    def minimu(self, p):
        if not p:
            return None
        while p.left:
            p = p.left
        return p.val

    def ismember(self, x):
        return self.find(x)

    def size(self):
        return self._size

    def find(self, x):
        p = self.root
        while p and p.val != x:
            if p.val > x:
                p = p.left
            else:
                p = p.right
        return p


def inorder(p, vec, i):
    if p.left:
        inorder(p.left, vec, i)
        vec[i + p.left.size] = p
    else:
        vec[i] = p
    if p.right:
        inorder(p.right, vec, i + p.size - p.right.size)


# if __name__ == '__main__':
#     B = grok_BST()
#     B.insert(1)
#     B.insert(-1)
#     B.insert(2)
#     B.insert(3)
#     B.insert(18)
#     B.insert(0)
#     B.erase(0)
#     B.erase(-1)
#     B.erase(18)
#     print(B.root.size)