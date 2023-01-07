//
//  grok_segmenttree.cpp
//  overload.cpp
//
//  Created by 胡泽弘 on 2022/11/15.
//

#include "grok_base.hpp"

using namespace std;

template<class _Tp>
class grok_SegmentTree{
public:
#define _start 1,n>>1,1
    grok_SegmentTree(int x, bool islazy = 0):_hrm(new grok_base::head()),islazy(islazy){
        for(n = 1;n < x;n<<=1);
        arr = vector<_Tp>(n|1 ,0);
        lazy = vector<_Tp>(n|1,0);
    
        if(!islazy)delete _hrm.sendto((new grok_base::act(1, 1))->push("SegmentTree")->push(n));
        else delete _hrm.sendto((new grok_base::act(1, 2))->push("SegmentTree")->push(n));
    }
    grok_SegmentTree(const grok_SegmentTree & sgt):_hrm(new grok_base::head()){
        arr = sgt.arr;
        lazy = sgt.lazy;
        n = sgt.n;
        islazy = sgt.islazy;
        if(!islazy)delete _hrm.sendto((new grok_base::act(1, 3))->push("SegmentTree")->push(arr));
        else delete _hrm.sendto((new grok_base::act(1, 4))->push("SegmentTree")->push(arr)->push(lazy));
    }
//    void operator = (const grok_SegmentTree & sgt){
//        arr = sgt.arr;
//        lazy = sgt.lazy;
//        n = sgt.n;
//        islazy = sgt.islazy;
//        if(!islazy)delete _hrm.sendto((new grok_base::act(1, 3))->push("SegmentTree")->push(arr));
//        else delete _hrm.sendto((new grok_base::act(1, 4))->push("SegmentTree")->push(arr)->push(lazy));
//    }
    void add(_Tp k,int x){
        if(x <= n && x > 0){
            add(k,x,_start);
            delete _hrm.sendto((new grok_base::act(3,1))->push(k)->push(x));
        }
        else perror("out of range");
    }
    void add(_Tp k,int l,int r){
        if(r <= n && l > 0){
            if(r < l){
                perror("wrong range");
                return;
            }
            if(l == r)add(k,l,_start);
            else add(k,l,r,_start);
            delete _hrm.sendto((new grok_base::act(3,2))->push(k)->push(l)->push(r));
        }
        else perror("out of range");
    }
    _Tp ask(int x){
        if(x <= n && x > 0)return ask(x,_start);
        else perror("out of range");
        return -1;
    }
    _Tp ask(int l,int r){
        if(r <= n && l > 0){
            if(r > l)perror("wrong range");
            else if(l == r)return ask(l,_start);
            else return ask(l,r,_start);
        }
        else perror("out of range");
        return -1;
    }
    size_t size(){
        return n;
    }
    bool empty(){
        return arr[1]==0;
    }
    ~grok_SegmentTree(){
        delete _hrm.sendto(new grok_base::act(-1));
    }
private:
#define _mid (left+right)>>1
#define _ls i<<1
#define _rs i<<1|1
#define _left left, mid, i<<1
#define _right mid+1, right, i<<1|1
    void add(_Tp k,int x,int left,int right,int i){
        arr[i] += k;
        if(left == right)return;
        int mid = _mid;
        if(mid >= x)add(k, x, _left);
        else add(k, x, _right);
    }
    void add(_Tp k,int l,int r,int left,int right,int i){
//        cout << l << " " << r << " " << i << endl;µ
        arr[i] += k*(r-l+1);
        if(islazy && left == l && right == r){
            if(left != right){
                lazy[_ls] += k;
                lazy[_rs] += k;
            }
            return;
        }
        if(left == right)return;
        int mid = (left+right)>>1;
        if(mid >= r)add(k, l, r, _left);
        else if(mid < l)add(k, l, r, _right);
        else{
            add(k, l, mid, _left);
            add(k, mid+1, r, _right);
        }
    }
    _Tp ask(int x,int left,int right,int i){
        if(islazy && lazy[i] != 0)lazyadjust(left, right, i);
        if(left == right)return arr[i];
        int mid = _mid;
        if(mid > x)return ask(x, _left);
        else return ask(x, _right);
    }
    _Tp ask(int l,int r,int left,int right,int i){
        if(islazy && lazy[i] != 0)lazyadjust(left, right, i);
        if(left == l && right == r)return arr[i];
        int mid = _mid;
        if(mid > r)return ask(l,r, _left);
        else if(mid < l)return ask(l,r, _right);
        else return ask(l, mid, _left) + ask(mid+1, r, _right);
    }
    void lazyadjust(int left,int right,int i){
        arr[i] += (right-left+1)*lazy[i];
        if(left != right){
            lazy[_ls] += lazy[i];
            lazy[_rs] += lazy[i];
        }
        lazy[i] = 0;
    }
    vector<_Tp> arr;
    vector<_Tp> lazy;
    int n;
    bool islazy;
    grok_base::msg _hrm;
};
