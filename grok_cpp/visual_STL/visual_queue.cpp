// 
//queue.cpp
//
//lzy 2022/11/17
//

#include <queue>
#include "../grok_base.hpp"
using namespace std;
//默认 0为无值 1为单值/双值 2为多值 3为重复多值
//-1 over
//1 init
//2 change
//3 push_back
//4 pop_back
//5 insert
//6 erase
//7 swap
//8 clear
template<class _Tp>
class visual_queue: public queue<_Tp>{
private:
    // friend class visual_queue;
    queue<_Tp> temp_q;
    grok_base::msg _hrm;
    _Tp _f,_b;
    void check(){
        if(!queue<_Tp> :: empty()){
            _Tp t = queue<_Tp> :: front();
            _Tp b = queue<_Tp> :: back();
            if(t != _f){
                delete _hrm.sendto((new grok_base::act(2,1))->push(0)->push(t));
                _f = t;
            }
            if(b != _b){
                delete _hrm.sendto((new grok_base::act(2,1))->push(1)->push(b));
                _b = b;
            }
        }
    }
public:
    visual_queue():queue<_Tp>(),_hrm(new grok_base::head()){
        delete _hrm.sendto((new grok_base::act(1, 0))->push("queue"));
    }
    visual_queue(const queue<_Tp>& _Cont):queue<_Tp>(_Cont),_hrm(new grok_base::head()){
        vector<_Tp> vec;
        for(auto & hhh : queue<_Tp> :: c){
            vec.push_back(hhh);
        }
        delete _hrm.sendto((new grok_base::act(1, 2))->push(vec)->push("queue"));
    }
    void push(_Tp x){
        check();
        queue<_Tp> :: push(x);
        _f = queue<_Tp> :: front();
        _b = queue<_Tp> :: back();
        delete _hrm.sendto((new grok_base::act(3, 1))->push(x));
    }
    void pop(){
        check();
        queue<_Tp> :: pop();
        if(queue<_Tp> :: empty()){
            _f = queue<_Tp> :: front();
            _b = queue<_Tp> :: back();
        }
        delete _hrm.sendto(new grok_base::act(4,0));
    }
    void swap(queue<_Tp> &x) {
        check();
        delete _hrm.sendto(new grok_base::act(8,0));
        queue<_Tp> :: swap(x);
        _f = queue<_Tp> :: front();
        _b = queue<_Tp> :: back();
        vector<_Tp> vec;
        for(auto & hhh : queue<_Tp> :: c){
            vec.push_back(hhh);
        }
        delete _hrm.sendto((new grok_base::act(1, 2))->push(vec));
    }
    void swap(visual_queue<_Tp> &x) {
        check();
        delete _hrm.sendto(new grok_base::act(8,0));
        x.check();
        delete x._hrm.sendto(new grok_base::act(8,0));

        vector<_Tp> vec;
        for(auto & hhh : visual_queue<_Tp> :: c){
            vec.push_back(hhh);
        }
        delete x._hrm.sendto((new grok_base::act(1, 2))->push(vec));
        queue<_Tp> :: swap(x);
        vec.clear();
        for(auto & hhh : visual_queue<_Tp> :: c){
            vec.push_back(hhh);
        }
        delete _hrm.sendto((new grok_base::act(1, 2))->push(vec));

        _f = queue<_Tp> :: front();
        _b = queue<_Tp> :: back();

        x._f = x.front();
        x._b = x.back();
    }
    void clear(){
        check();
        queue<_Tp> :: clear();
        delete _hrm.sendto(new grok_base::act(8,0));
    }
    _Tp& front(){
        check();
        return queue<_Tp> :: front();
    }
    _Tp& back(){
        check();
        return queue<_Tp> :: back();
    }
    ~visual_queue(){
        check();
        delete _hrm.sendto(new grok_base::act(-1));
    }
};

