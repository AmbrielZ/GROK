//
//  grok_segmenttree.cpp
//  overload.cpp
//
//  Created by AmbrielZ on 2022/11/15.
//

#include "grok_base.hpp"

using namespace std;

template<class _Tp>
class grok_SegmentTree{
public:
#define _start 1,n,1
    grok_SegmentTree(int x = 0):_hrm(new grok_base::head()){
        for(n = 1;n < x;n<<=1);
        arr = vector<_Tp>(n<<1|1,0);
        lazy = vector<_Tp>(n<<1|1,0);
        
        delete _hrm.sendto((new grok_base::act(1, 0))->push("SegmentTree")->push(n));
    }
    void add(_Tp k,int x){
        if(x <= n && x > 0){
            add(k,x,_start);
            delete _hrm.sendto((new grok_base::act(3,1))->push(k)->push(x));
        }
        else perror("out of range");
    }
    void add(_Tp k,int l,int r){
        if(r <= n && l > 0){
            if(r > l){
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
#define _left left, mid, _ls
#define _right mid+1, right, _rs
    void add(_Tp k,int x,int left,int right,int i){
        arr[i] += k;
        if(left == right)return;
        int mid = _mid;
        if(mid > x)add(k, x, _left);
        else add(k, x, _right);
    }
    void add(_Tp k,int l,int r,int left,int right,int i){
        arr[i] += k*(r-l+1);
        if(left == l && right == r){
            if(left != right){
                lazy[_ls] += k;
                lazy[_rs] += k;
            }
            return;
        }
        int mid = (left+right)>>1;
        if(mid >= r)add(k, l, r, _left);
        else if(mid < l)add(k, l, r, _right);
        else{
            add(k, l, mid, _left);
            add(k, mid+1, r, _right);
        }
    }
    _Tp ask(int x,int left,int right,int i){
        if(lazy[i] != 0)lazyadjust(left, right, i);
        if(left == right)return arr[i];
        int mid = _mid;
        if(mid > x)return ask(x, _left);
        else return ask(x, _right);
    }
    _Tp ask(int l,int r,int left,int right,int i){
        if(lazy[i] != 0)lazyadjust(left, right, i);
        if(left == l && right == r)return arr[i];
        int mid = _mid;
        if(mid >= r)return ask(l,r, _left);
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
    grok_base::msg _hrm;
};

