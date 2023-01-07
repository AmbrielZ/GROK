from bst import *


class scapegoat(grok_BST):
    def __init__(self):
        super().__init__("scapegoat")
        self.alpha = 0.7

    def find(self, x):
        p = self.root
        q = None
        tracker = ''
        while p and p.val != x:
            if p.unbalanced(self.alpha):
                vec = {}
                self.__inorder(p, vec, 0)
                p = self.__buildtree(vec, 0, p.size - 1)
                if q:
                    if x < q.val:
                        q.left = p
                    else:
                        q.right = p
                else:
                    self.root = p
                self._hrm.sendto(act(9, 1).push(tracker))
            q = p
            if x > p.val:
                tracker += '1'
            else:
                tracker += '0'
            if x > p.val:
                p = p.right
            else:
                p = p.left
        return p

    def insert(self, x):
        if self.find(x):
            return 0
        self._hrm.sendto(act(5, 1).push(x))
        p = self.root
        while p:
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
        return 1

    def erase(self, x):
        if self.find(x):
            return
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

    def size(self):
        if self.root:
            return self.root.size
        else:
            return 0

    def __buildtree(self, vec, left, right):
        if left > right:
            return None
        mid = (left + right) >> 1
        p = vec[mid]
        p.left = self.__buildtree(vec, left, mid - 1)
        p.right = self.__buildtree(vec, mid + 1, right)
        p.resize()
        return p

    def __inorder(self, p, vec, i):
        if p.left:
            self.__inorder(p.left, vec, i)
            vec[i + p.left.size] = p
        else:
            vec[i] = p
        if p.right:
            self.__inorder(p.right, vec, i + p.size - p.right.size)


if __name__ == '__main__':
    s = scapegoat()
    for i in range(12):
        s.insert(i)
