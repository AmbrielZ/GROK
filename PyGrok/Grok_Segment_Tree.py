from PyGrokbase import *

import sys
sys.setrecursionlimit(100000) #例如这里设置为十万


def tail_call_optimized(func):
    def _wrapper(*args, **kwargs):
        f = sys._getframe()
        if f.f_back and f.f_back.f_back and f.f_code == f.f_back.f_back.f_code:
            raise TailCallException(args, kwargs)

        else:
            while True:
                try:
                    return func(*args, **kwargs)
                except TailCallException as e:
                    args = e.args
                    kwargs = e.kwargs
    return _wrapper

class SegmentTree:
    def __init__(self, x, islazy = False):
        """线段树相当于将数组用一棵树重新表示"""

        self._arr = []
        self._lazy = []
        self._islazy = islazy
        self._hrm = msg(head());
        self._sum = 0;
        self._n = 1;
        while self._n < x:
            self._n <<= 1
        self._arr = [0]*(self._n|1)
        self._lazy = [0]*(self._n|1)
        if self._islazy == 0 :
            self._hrm.sendto(act(1,1).push("SegmentTree "+str(self._n)))
            print("1,1","SegmentTree "+str(self._n))
        else :
            self._hrm.sendto(act(1, 2).push("SegmentTree " + str(self._n)))
            print("1,2","SegmentTree " + str(self._n))
    def add(self,k, x):
        if x <= self._n and x > 0 :
            self._add(k,x,1,self._n>>1,1)
            self._hrm.sendto(act(3,1).push(k).push(x))
            print(3,1,k,x)
        else:
            raise MemoryError('out of range')
    def addSection(self ,k, l, r):
        if r <=self._n and l >0 :
            if r < l :
                raise MemoryError('wrong range')
                return
            if l == r:
                self._addSection(k, l ,1,self._n>>1,1)
            else:
                self._addSection(k,l,r,1,self._n>>1,1)
            self._hrm.sendto(act(3,2).push(k).push(l).push(r))
            print(3,2,k,l,r)
        else:
            raise MemoryError("out of range")
    def ask(self, x):
        if x<=self._n and x >0 :
            return  self._ask(x,1,self._n>>1,1);
        else:
            raise MemoryError("out of range")
            return -1;

    def askSection(self,l , r):
        if r<=self._n and l>0:
            if r<l :
                raise MemoryError("out of range")
            elif l==r:
                return self._ask(l,1,self._n>>1,1)
            else:
                return self.askSection1(l,r,1,self._n>>1,1)
        else:
            raise MemoryError("out of range")
        return -1;


    def __sizeof__(self):
        return self._n;

    def empty(self):
        return self._arr[1]==0;

    def __del__(self):
        self._hrm.sendto(act(-1,0))
        print(-1,0)

    def _add(self, k,x, left,right,i) :
        self._arr[i] += k;
        if left==right:
            return
        mid = (left+right)>>1
        if mid >=x :
            self._add(k,x,left, mid, i<<1)
        else:
            self._add(k,x,mid+1, right, i<<1|1)

    def _addSection(self,k,l,r,left,right,i):
        #print(l," ",r," ",i)
        self._arr[i] += k*(r-l+1)
        if self._islazy and left == l and right == r :
            if left != right :
                self._lazy[i<<1] += k
                self._lazy[i<<1|1] += k
            return
        if left==right :
            return
        mid = (left + right) >> 1;
        if mid >= r:
            self._addSection(k,l,r,left, mid, i<<1)
        elif mid<l:
            self._addSection(k,l,r,mid+1, right, i<<1|1)
        else:
            self._addSection(k,l,mid,left, mid, i<<1)
            self._addSection(k,mid+1,r,mid+1, right, i<<1|1)

    def askSection1(self,l,r,left,right,i):
        self._sum = 0;
        self._askSection(l,r,left,right,i)
        return self._sum


    def _ask(self,x,left,right,i):
        #print(x,left,right,i)
        if self._islazy and self._lazy[i] !=0:
            self.lazyadjust(left,right,i)
        if left == right:
            #print(self._arr[i])
            return self._arr[i]
        mid = (left+right) >>1
        if mid >=x:
            return self._ask(x,left, mid, i<<1)
        else:
            return self._ask(x,mid+1, right, i<<1|1)


    #@tail_call_optimized
    def _askSection(self, l, r, left, right, i):
        if i >=self._n :
            return
        if self._islazy and self._lazy[i] != 0:
            self.lazyadjust(left, right, i)
        if left == l and right == r:
            self._sum += self._arr[i]
            #print(l,r,left,right,i,self._sum)
            return

        mid = (left + right) >> 1
        #print(l, r, mid, left, right, i)

        if mid > r:
             self._askSection(l, r, left, mid, i << 1)
        elif mid < l:
             self._askSection(l, r, mid + 1, right, i << 1 | 1);
        else:
            self._askSection(l, mid, left, mid, i << 1)
            self._askSection(mid + 1, r, mid + 1, right, i << 1 | 1);


    def lazyadjust(self,left,right,i):
        self._arr[i] += (right-left+1)*self._lazy[i]
        if left != right:
            self._lazy[i<<1] += self._lazy[i];
            self._lazy[i << 1|1] += self._lazy[i];
        self._lazy[i] = 0;

    def __str__(self):
        res = []
        res.append('[')
        for i in range(len(self._arr) -1):
            res.append(str(self._arr[i+1]))
            if i != len(self._arr) - 2:
                res.append(', ')
        res.append(']')
        return '<SegmentTree>: ' + ''.join(res)

import sys

class TailCallException(BaseException):
    def __init__(self, args, kwargs):
        self.args = args
        self.kwargs = kwargs



if __name__ == '__main__':
     s = SegmentTree(10,True)
     print(s)
     s.addSection(7, 4, 7)
     s.add(2,2)
     print(s)
     print(s)
     x = s.ask(1)
     print(s.ask(1),s.ask(2),s.ask(3))
     print(s.askSection(1,3))