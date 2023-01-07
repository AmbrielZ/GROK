//
//  visual_set.cpp
//  overload.cpp
//
//  Created by 胡泽弘 on 2022/12/23.
//

#include <set>
#include "../grok_base.hpp"
using namespace std;
template <class _Key, class _Compare = less<_Key>,
          class _Allocator = allocator<_Key> >
class visual_set:public set<_Key,_Compare,_Allocator>{
public:
    visual_set():_hrm(new grok_base::head()),set<_Key,_Compare,_Allocator>(){
        delete _hrm.sendto((new grok_base::act(1, 0))->push("rbt"));
    }
    grok_base::msg _hrm;
    void insert(_Key __v){
        if(set<_Key,_Compare,_Allocator>::find(__v) != set<_Key,_Compare,_Allocator>::end())return;
        set<_Key,_Compare,_Allocator>::insert(__v);
        delete _hrm.sendto((new grok_base::act(5,1))->push(__v));
    }
    void erase(_Key __v){
        set<_Key,_Compare,_Allocator>::erase(__v);
        delete _hrm.sendto((new grok_base::act(6,1))->push(__v));
    }
    void clear(){
        set<_Key,_Compare,_Allocator>::clear();
        delete _hrm.sendto(new grok_base::act(8,0));
    }
    ~visual_set(){
        _hrm.sendto(new grok_base::act(-1));
    }
};
