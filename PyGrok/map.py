# 再红黑树的实现过程中，要考虑父节点的父节点不一定存在的问题
# 定义树节点类
from PyGrokbase import *


class Node(object):
    def __init__(self, key, value) -> None:
        self.key = key
        self.value = value
        self.color = 'r'
        self.father = None
        self.left = None
        self.right = None


# 定义红黑树类
class Map(object):
    def __init__(self, node: Node) -> None:
        self.root = node
        node.rcolor('b')
        self._hrm = msg(head())
        self._hrm.sendto(act(1, 0).push("map"))
        # 基于传入的根节点实例化红黑树

    def __init__(self) -> None:
        self.root = None
        self._hrm = msg(head())
        self._hrm.sendto(act(1, 0).push("map"))
        # 无参构造函数

    def insert(self, node: Node) -> None:
        if self.root == None:
            node.color = 'b'
            self.root = node
            return
        # 不为空树
        currentNode = self.root
        while True:
            if node.key < currentNode.key:
                if currentNode.left == None:
                    currentNode.left = node
                    node.father = currentNode
                    break
                else:
                    currentNode = currentNode.left
            else:
                if currentNode.right == None:
                    currentNode.right = node
                    node.father = currentNode
                    break
                else:
                    currentNode = currentNode.right
        # 插入结束开始进行平衡操作
        self.__insertBalance(node)
        self._hrm.sendto(act(5, 1).push(node.key).push(node.value))

    def __insertBalance(self, node: Node):
        # 插入平衡函数
        pNode = node.father
        if pNode == None:
            # 该节点为根节点
            node.color = 'b'
            return
        if pNode.color == 'b':
            return
        gNode = pNode.father
        flag1 = 0 if gNode.left == pNode else 1
        unode = gNode.left if flag1 else gNode.right
        if unode == None:
            flag2 = 0 if pNode.left == node else 1
            pgNode = gNode.father
            if pgNode:
                flag3 = 0 if pgNode.left == gNode else 1
            else:
                flag3 = 2  # 此时pgNode不存在
            if flag1 == 0 and flag2 == 0:
                # 父左子左
                pNode.right = gNode
                pNode.color = 'b'
                if flag3 == 1:
                    pgNode.right = pNode
                    pNode.father = pgNode
                elif flag3 == 0:
                    pgNode.left = pNode
                    pNode.father = pgNode
                else:
                    # 曾祖父节点不存在，旋转之后红黑树的根节点发生改变
                    self.root = pNode
                gNode.color = 'r'
                gNode.father = pNode
                gNode.left = None
            elif flag1 == 1 and flag2 == 1:
                # 父右子右
                pNode.color = 'b'
                pNode.left = gNode
                if flag3 == 1:
                    pgNode.right = pNode
                    pNode.father = pgNode
                elif flag3 == 0:
                    pgNode.left = pgNode
                    pNode.father = pgNode
                else:
                    # 此时根节点发生改变
                    self.root = pNode
                    pNode.father = None
                gNode.color = 'r'
                gNode.father = pNode
                gNode.right = None
            elif flag1 == 0 and flag2 == 1:
                # 父左子右
                gNode.left = node
                node.father = gNode
                node.left = pNode
                pNode.father = node
                pNode.right = None
                self.__insertBalance(pNode)
            elif flag1 == 1 and flag2 == 0:
                # 父右子左
                gNode.right = node
                node.father = gNode
                node.right = pNode
                pNode.father = node
                pNode.left = None
                self.__insertBalance(pNode)
        else:
            pNode.color = 'b'
            unode.color = 'b'
            gNode.color = 'r'
            self.__insertBalance(gNode)
        return

    def find(self, key):
        # 首先搜索节点，判断该节点是否存在
        if self.root == None:
            # 该树为空树
            return
        currentNode = self.root
        while currentNode:
            if currentNode.key == key:
                break
            elif currentNode.key > key:
                currentNode = currentNode.left
            else:
                currentNode = currentNode.right
        if currentNode == None:
            # 该节点不存在
            return
        else:
            return currentNode

    def erase(self, key):
        # 首先搜索节点，判断该节点是否存在
        if self.root == None:
            # 该树为空树
            return
        currentNode = self.root
        while currentNode:
            if currentNode.key == key:
                break
            elif currentNode.key > key:
                currentNode = currentNode.left
            else:
                currentNode = currentNode.right
        if currentNode == None:
            # 该节点不存在
            return
        dnode = currentNode  # 待删除节点
        self.__delete(dnode)  # 节点删除完毕
        self._hrm.sendto(act(6, 1).push(dnode.key))

    def __delete(self, dnode: Node):
        if dnode.left == None and dnode.right == None:
            if dnode.color == 'r':
                # 红色的叶子节点
                pnode = dnode.father
                if pnode.left == dnode:
                    pnode.left = None
                else:
                    pnode.right = None
            else:
                pnode = dnode.father
                if pnode == None:
                    self.root == None
                    return
                # 先执行平衡操作，再删除节点
                self.__delete_blackleaf_balance(dnode)
                if pnode.left == dnode:
                    pnode.left = None
                else:
                    pnode.right = None
                # 黑色的叶子节点
        elif dnode.left == None and dnode.right:
            # 删除节点含有一个右子节点，对应黑红
            pnode = dnode.father
            cnode = dnode.right
            print("xxxx", pnode.key)
            if pnode.left == dnode:
                pnode.left = cnode
            else:
                pnode.right = cnode
            cnode.father = pnode
            cnode.color = 'b'
        elif dnode.left and dnode.right == None:
            # 删除节点含有一个左子节点，对应黑红
            pnode = dnode.father
            cnode = dnode.left
            if pnode.left == dnode:
                pnode.left = cnode
            else:
                pnode.right = cnode
            cnode.father = pnode
            cnode.color = 'b'
        else:
            # 删除节点，含有两个子节点
            # 用前驱节点替换，转情况1、2、3
            prenode = dnode.left
            while prenode.right:
                prenode = prenode.right
            dnode.key = prenode.key
            self.__delete(prenode)

    def __delete_blackleaf_balance(self, dnode: Node) -> None:
        if dnode.father == None:
            return
        pnode = dnode.father
        flag1 = 0 if pnode.left == dnode else 1
        if flag1:
            snode = pnode.left
        else:
            snode = pnode.right
        if snode.color == 'b':
            # 兄弟节点为黑色
            if snode.left == None and snode.right == None:
                # 兄弟节点的两个子节点全黑
                if pnode.color == 'b':
                    # 父节点为黑
                    snode.color = 'r'
                    self.__delete_blackleaf_balance(pnode)
                else:
                    # 父节点为红色
                    pnode.color = 'b'
                    snode.color = 'r'
                    return
            else:
                # 兄弟节点的子节点不为全黑
                if flag1:
                    # snode为pnode的左子节点
                    if snode.left == None:
                        # sl为黑色
                        sl, sr = snode.left, snode.right
                        pnode.left = sr
                        sr.father = pnode
                        sr.color = 'b'
                        sr.left = snode
                        snode.father = sr
                        snode.color = 'r'
                        snode.right = None
                        self.__delete_blackleaf_balance(dnode)
                    else:
                        # sl为红色
                        gnode = pnode.father
                        if gnode:
                            flag2 = 0 if gnode.left == pnode else 1
                        else:
                            flag2 = 2
                        if flag2 == 1:
                            gnode.right = snode
                        elif flag2 == 0:
                            gnode.left = snode
                        else:
                            # 祖父节点不存在，此时树的根节点由pnode变为snode
                            self.root = snode
                        snode.color, pnode.color = pnode.color, snode.color
                        snode.father = gnode
                        sl, sr = snode.left, snode.right
                        snode.right = pnode
                        pnode.father = snode
                        pnode.left = sr
                        sl.color = 'b'
                        if sr:
                            sr.father = pnode
                        return
                else:
                    # snode为pnode的右子节点
                    if snode.right == None:
                        # sr为黑色
                        sl, sr = snode.left, snode.right
                        pnode.right = sl
                        sl.father = pnode
                        sl.color = 'b'
                        sl.right = snode
                        snode.father = sl
                        snode.color = 'r'
                        snode.left = None
                        self.__delete_blackleaf_balance(dnode)
                    else:
                        # sr为红色
                        gnode = pnode.father
                        if gnode:
                            flag2 = 0 if gnode.left == pnode else 1
                        else:
                            flag2 = 2
                        if flag2 == 1:
                            gnode.right = snode
                        elif flag2 == 0:
                            gnode.left = snode
                        else:
                            # 祖父节点不存在，此时树的根节点由pnode变为snode
                            self.root = snode
                        snode.color, pnode.color = pnode.color, snode.color
                        snode.father = gnode
                        sl, sr = snode.left, snode.right
                        snode.left = pnode
                        pnode.father = snode
                        pnode.right = sl
                        sr.color = 'b'
                        if sl:
                            sl.father = pnode
                        return
        else:
            # 兄弟节点为红色
            gnode = pnode.father
            sl, sr = snode.left, snode.right
            flag2 = 0 if gnode.left == pnode else 1
            if flag2:
                gnode.right = snode
            else:
                gnode.left = snode
            snode.father = gnode
            snode.color = 'b'
            pnode.color = 'r'
            pnode.father = snode
            if flag1:
                # 兄弟节点为左子节点
                snode.right = pnode
                pnode.left = sr
                sr.father = pnode
            else:
                # 兄弟节点为右子节点
                snode.left = pnode
                pnode.right = sl
                sl.father = pnode
            self.__delete_blackleaf_balance(dnode)

    def clear(self):
        self._hrm.sendto(act(8, 0))

    def __del__(self):
        self._hrm.sendto(act(-1, 0))


# 红黑树中序遍历
def mid(root: Node):
    if root == None:
        return
    mid(root.left)
    if root.left:
        left = root.left.key
    else:
        left = None
    if root.right:
        right = root.right.key
    else:
        right = None
    if root.father:
        f = root.father.key
    else:
        f = None
    print(root.key, root.color, f, left, right)
    mid(root.right)


# 代码测试
if __name__ == '__main__':
    data = [10, 20, 15, 30]
    rd = Map()
    for x in data:
        node = Node(x, 1)
        rd.insert(node)
    rd.erase(10)
    mid(rd.root)










