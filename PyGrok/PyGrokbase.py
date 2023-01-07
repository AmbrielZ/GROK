import socket


class grok_udp:
    def __init__(self):
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.local_addr = ("127.0.0.1", 7851)

    def sendto(self, __msg_):
        self.udp_socket.sendto(__msg_, self.local_addr)
        # sprintf(__msg_buf, "%s",__msg_.c_str());
        # ::sendto(__client_sock, __msg_buf, strlen(__msg_buf), 0, (sockaddr*)(&__addr), sizeof(__addr));
        # memset(__msg_buf, 0, _buf_);


udp = grok_udp()
g_count = 1


class head:
    def __init__(self):
        global g_count
        self.gid = g_count
        g_count += 1

    def put(self):
        return str(self.gid)


class act:
    def __init__(self, _x, _y):
        self.type = str(_x)
        self.subtype = str(_y)
        self.datas = str()

    def push(self, paras):
        self.datas += ' ' + str(paras)
        return self

    def push_list(self, paras):
        for cur in paras:
            self.datas += ' ' + str(cur)
        return self

    def put(self):
        return self.type + ' ' + self.subtype + self.datas


class msg:
    def __init__(self, _h):
        self._head = _h

    def sendto(self, _act: act):
        global udp
        print((self._head.put() + ' ' + _act.put()).encode())
        udp.sendto((self._head.put() + ' ' + _act.put()).encode())



class grok_TreeNode:
    def __init__(self, _x = 0.0, _l = None, _r = None):
        self.val = _x
        self.left = _l
        self.right = _r
        self.size = 1 + (_l.size if _l is not None else 0) + (_r.size if _r is not None else 0)

    #scapegoat
    def unbalanced(self, alpha):
        return ((self.left is not None and self.left.size > alpha*self.size)
                or (self.right and self.right.size > alpha*self.size))

    def resize(self):
        self.size = 1 + (self.left.size if self.left is not None else 0) + \
                    (self.right.size if self.right is not None else 0)

def inorder(p):
    if p is None:
        return None
    inorder(p.left)
    print(p.val)
    inorder(p.right)

