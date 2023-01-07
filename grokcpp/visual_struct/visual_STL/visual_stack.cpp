//
//  stack.cpp
//
//  lypoom 221114
//

#include <stack>
#include <deque>
#include "../grok_base.hpp"

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

using namespace std;
template<class _Tp>
class visual_stack: public stack<_Tp>{
private:
    _Tp _y;
    grok_base::msg _hrm;
    void check(){
        if(stack<_Tp> :: empty())return;
        _Tp t = stack<_Tp> :: top();
        if(t == _y)return;
        delete _hrm.sendto((new grok_base::act(2,1))->push(t));
        _y = t;
    }
public:
    visual_stack():stack<_Tp>(),_hrm(new grok_base::head()){
        delete _hrm.sendto((new grok_base::act(1, 0))->push("stack"));
    }
    void push(_Tp x){
        check();
        stack<_Tp> :: push(x);
        _y = x;
        delete _hrm.sendto((new grok_base::act(3,1))->push(x));

    }
    void pop(){
        check();
        stack<_Tp> :: pop();
        if(!stack<_Tp> :: empty())_y = stack<_Tp> :: top();
        delete _hrm.sendto(new grok_base::act(4,0));

    }
//    typename deque<_Tp>::reference& top(){
//        check();
//        return stack<_Tp> :: top();
//    }
    void clear()
    {
        check();
        stack<_Tp> :: clear();
        delete _hrm.sendto(new grok_base::act(8,0));
    }
    ~visual_stack(){
        check();
        delete _hrm.sendto(new grok_base::act(-1));
    }
};
