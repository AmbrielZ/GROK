#include<map>
#include "grok_base.hpp"
using namespace std;

template <class _Kty, class _Ty, class _Pr = less<_Kty>, class _Alloc = allocator<pair<const _Kty, _Ty>>>
class visual_map : public map<_Kty, _Ty, _Pr, _Alloc>{
public:
    visual_map():
    _hrm(new grok_base::head()),
    map<_Kty,_Ty,_Pr,_Alloc>(){}
    void insert(pair<_Kty, _Ty> _Val) {
        map<_Kty, _Ty> :: insert(_Val);
        delete _hrm.sendto((new grok_base::act(5,1))->push(_Val.first)->push(_Val.second));
    }

    void erase(_Kty _Keyval){
        map<_Kty, _Ty> :: erase(_Keyval);
        delete _hrm.sendto((new grok_base::act(6,1))->push(_Keyval));
    }

    void clear(){
        map<_Kty, _Ty> :: clear();
        delete _hrm.sendto((new grok_base::act(8,0)));
    }

    ~visual_map(){
//        delete _hrm.sendto(new grok_base::act(-1));
    }
    grok_base::msg _hrm;
};
