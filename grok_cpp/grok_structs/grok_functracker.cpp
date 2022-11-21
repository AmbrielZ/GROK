//
//  grok_functracker.cpp
//
//  Created by AmbrielZ on 2022/11/21.
//

#include "grok_base.hpp"
using namespace std;

class grok_funcTracker{
public:
    grok_funcTracker(const string & name, const string & in_name = "x",const string & out_name = "f(x)")
    { delete _hrm.sendto((new grok_base::act(1,1))->push("FunTrack")->push(name)->push(in_name)->push(out_name)); }
    
    template<class _inTp>
    _inTp & in(const _inTp & ret,string * trans_fun(...) = NULL, ...){
        delete _hrm.sendto((new grok_base::act(3,1))->push(0)->push(trans_fun ?trans_fun(ret) : ret));
        return ret;
    }
    
    template<class _outTp>
    _outTp & out(const _outTp & ret,string * trans_fun(...) = NULL, ...){
        delete _hrm.sendto((new grok_base::act(3,1))->push(1)->push(trans_fun ?trans_fun(ret) : ret));
        return ret;
    }
private:
    grok_base::msg _hrm;
};

int main(){
    return 0;
}
