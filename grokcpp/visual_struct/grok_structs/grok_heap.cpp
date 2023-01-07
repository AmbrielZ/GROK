//
//  grok_heap.cpp
//  overload.cpp
//
//  Created by 胡泽弘 on 2022/11/17.
//

#include "grok_base.hpp"
using namespace std;

template <class _Tp, class _Compare = less<_Tp>>
class grok_Heap{
public:
    grok_Heap():_n(0),_hrm(new grok_base::head()){
        delete _hrm.sendto((new grok_base::act(1,0))->push("Heap"));
    };
    grok_Heap(const vector<_Tp> & arr):_n(arr.size()),_hrm(new grok_base::head()){
        delete _hrm.sendto((new grok_base::act(1,0))->push("Heap"));
        for(int i = 0;i < _n;i++)push(arr[i]);
    }
    void push(_Tp x){
        if(_n == _vec.size())_vec.push_back(0);
        insert(x, _n++);
    }
    _Tp pop(){
        swap(front(), _vec[--_n]);
        int i = 0;_Tp cur = _vec[0];
        for(int j = 1;j < _n;j<<=1, j++){
            if(j + 1 < _n && _Compare()(_vec[j], _vec[j+1]))j++;
            if(!_Compare()(cur, _vec[j]))break;
            _vec[i] = _vec[j];
            i = j;
        }
        _vec[i] = cur;
        delete _hrm.sendto(new grok_base::act(4,0));
        return _vec[_n];
    }
    _Tp & front(){
        if(empty())perror("Heap is empty");
        return _vec[0];
    }
    bool empty(){
        return _n == 0;
    }
    ~grok_Heap(){
        delete _hrm.sendto(new grok_base::act(-1,0));
    }
private:
    void insert(_Tp x,size_t i){
        while(i > 0 &&  _Compare()(_vec[(i-1)>>1],x)){
            _vec[i] = _vec[(i-1)>>1];
            (--i)>>=1;
        }
        _vec[i] = x;
        delete _hrm.sendto((new grok_base::act(3,1))->push(x));
    }
    vector<_Tp> _vec;
    size_t _n;
    grok_base::msg _hrm;
};
