//
//  visual_vector.cpp
//  overload.cpp
//
//  Created by AmbrielZ on 2022/11/15.
//

#include "grok_base.hpp"

using namespace std;
template<class _Tp, class _Allocator = allocator<_Tp>>
class visual_vector: public vector<_Tp>{
private:
    int _x;
    _Tp _y;
    grok_base::msg _hrm;
    typedef __vector_base<_Tp, _Allocator>           __base;
    typedef typename __base::const_pointer           const_pointer;
    typedef __wrap_iter<const_pointer>               const_iterator;
    
    void check(){
        if(_x >= 0){
            _Tp tmp = vector<_Tp> :: operator[](_x);
            if(tmp != _y)
                delete _hrm.sendto((new grok_base::act(2,1))->push(_x)->push(tmp));
            _x = -1;
        }
    }
public:
    visual_vector():vector<_Tp>(),_x(-1),_hrm(new grok_base::head()){
        delete _hrm.sendto((new grok_base::act(1, 0))->push("vector"));
    }
    visual_vector(size_t _n):vector<_Tp>(_n, 0),_hrm(new grok_base::head()),_x(-1){
        delete _hrm.sendto((new grok_base::act(1, 4))->push("vector")->push(_n)->push(0));
    }
    visual_vector(size_t _n, _Tp _x):vector<_Tp>(_n,_x),_hrm(new grok_base::head()),_x(-1){
        delete _hrm.sendto((new grok_base::act(1, 4))->push("vector")->push(_n)->push(_x));
    }
    _Tp & operator [](size_t __n){
        check();
        _Tp & t = vector<_Tp> :: operator[](__n);
        _x = (int)__n, _y = t;
        return t;
    }
    void push_back(_Tp x){
        check();
        vector<_Tp> :: push_back(x);
        delete _hrm.sendto((new grok_base::act(3,1))->push(x));
    }

    void emplace_back(_Tp x){
        check();
        vector<_Tp> :: push_back(x);
        delete _hrm.sendto(new grok_base::act(3,1))->push(x);
    }
    
    void pop_back(){
        check();
        vector<_Tp> :: pop_back();
        delete _hrm.sendto(new grok_base::act(4,0));
    }
    
    typename vector<_Tp, _Allocator>::iterator insert(const_iterator __position, _Tp&& __x){
        check();


        size_t _l = (__position - this->begin());
        auto it = (vector<_Tp> :: insert(__position, __x));

        stringstream ss;
        ss << "insert " << _l << ' ' << __x;
        delete _hrm.sendto((new grok_base::act(5,1))->push(_l)->push(__x));
        return it;
    }
    
    template <class _InputIterator>
    typename vector<_Tp, _Allocator>::iterator
    insert(const_iterator __position, _InputIterator __first, _InputIterator __last){
        check();

        size_t _l = (__position - this->begin());
        auto it =vector<_Tp> :: insert(__position, __first, __last);

        vector<_Tp> __vec_(_l);
        __vec_.insert(__vec_.begin()+_l ,__first, __last);
        delete _hrm.sendto((new grok_base::act(5,2))->push(__vec_));
        return it;
    }

    typename vector<_Tp, _Allocator>::iterator insert(const_iterator __position,int __n,_Tp&& __x){
        check();

        size_t _l = (int)(__position - this->begin());
        auto it = vector<_Tp> :: insert(__position,__n ,__x);

        delete _hrm.sendto((new grok_base::act(5,3))->push(_l)->push(__n)->push(__x));
        return it;
    }

    typename vector<_Tp, _Allocator>::iterator erase(const_iterator __position){
        check();

        size_t _l = (int)(__position - this->begin());
        auto it = vector<_Tp> :: erase(__position);

        delete _hrm.sendto((new grok_base::act(6,1))->push(_l));
        return it;
    }
    typename vector<_Tp, _Allocator>::iterator erase(const_iterator __first, const_iterator __last){
        check();

        size_t _f = (int)(__first - this->begin()), _l = (int)(__last - this->begin());
        auto it = vector<_Tp> :: erase(__first, __last);

        delete _hrm.sendto((new grok_base::act(6,2))->push(_f)->push(_l));
        return it;
    }
    void swap(size_t i, size_t j){
        check();

        std::swap(vector<_Tp> :: operator[](i), vector<_Tp> :: operator[](j));

        delete _hrm.sendto((new grok_base::act(7,1))->push(i)->push(j));
    }
    void clear(){
        check();

        vector<_Tp> :: clear();

        delete _hrm.sendto(new grok_base::act(8,0));
    }
    //    void assign(size_t __n,const _Tp && __u){
    //        check();
    //
    //        vector<_Tp> :: assign(__n, __u);
    //
    //        stringstream ss;
    //        ss << "change_1 " << __n << ' ' << __u;
    //        sendto(ss.str());
    //    }
    //    template <class _InputIterator>
    //    void assign(_InputIterator __first, _InputIterator __last){
    //        check();
    //
    //        vector<_Tp> :: assign(__first, __last);
    //
    //        stringstream ss;
    //        ss << ((__last - __first) > this->size() ? "init_1" : "change_2");
    //        for(_InputIterator c = __first;c < __last;c++)ss << ' ' << (*c);
    //        sendto(ss.str());
    //
    //    }
    ~visual_vector(){
        check();
        _hrm.sendto(new grok_base::act(-1));
    }
};

