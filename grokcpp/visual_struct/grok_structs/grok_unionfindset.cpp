//
//  grok_unionfindset.cpp
//  overload.cpp
//
//  Created by 胡泽弘 on 2022/11/28.
//

#include "../grok_base.hpp"

using namespace std;

class UnionFindSet{
public:
    UnionFindSet(size_t _n): n(_n), setCount(_n), parent(_n), size(_n, 1),_hrm(new grok_base::head()){
        for(int i = 0;i < _n;i++)parent[i] = i;
        delete _hrm.sendto((new grok_base::act(1, 4))->push("unionfindset")->push(_n));
    }
    
    
    ~UnionFindSet(){
        delete _hrm.sendto(new grok_base::act(-1, 0));
    }

    int findset(int x) {
        return parent[x] == x ? x : parent[x] = findset(parent[x]);
    }

    bool unite(int x, int y) {
        delete _hrm.sendto((new grok_base::act(3, 1))->push(x)->push(y));
        x = findset(x);
        y = findset(y);
        if(x == y)return 0;
        if(size[x] < size[y])swap(x, y);
        parent[y] = x;
        size[x] += size[y];
        --setCount;
        
        return 1;
    }
    bool connected(int x, int y) {
        x = findset(x);
        y = findset(y);
        return x == y;
    }
private:
    grok_base::msg _hrm;
    vector<int> parent;
    vector<int> size;
    size_t n;
    size_t setCount;
};
