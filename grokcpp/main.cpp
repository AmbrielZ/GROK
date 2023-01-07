

#include <iostream>
//#include "msg.pb.h"
#include "visual_struct/grok_struct.hpp"


using namespace std;

void QuickSort(visual_vector<int> & vec,int left,int right);

int main(int argc, const char * argv[]) {
    grok_SegmentTree<int> Seg(10);
    Seg.add(2, 2);
    Seg.add(7, 1, 3);
    grok_SegmentTree<int> sgt(Seg);
    grok_SegmentTree<int> Sgg(10, 1);
    Sgg.add(2, 2);
    Sgg.add(7, 4, 6);

    grok_BST<int> b;
    grok_scapegoat<int> sc;
    grok_scapegoat<int> sc2(0.5);
    visual_set<int> se;
    for(int i = 4;i >= 0;i--){
        b.insert(i);
        sc.insert(i);
        sc2.insert(i);
        se.insert(i);
    }
    for(int i = 1;i < 4;i++){
        b.insert(i*79%17);
        sc.insert(i*79%17);
        sc2.insert(i*79%17);
        se.insert(i*79%17);
    }
    for(int i = 1;i < 4;i++){
        b.erase(i*79%17);
        sc.insert(i*79%17);
        sc2.insert(i*79%17);
        se.insert(i*79%17);
    }
    
    UnionFindSet self(10);
    self.unite(0, 1);
    self.unite(2, 3);
    self.unite(0, 2);
    self.unite(4, 5);
    self.unite(5, 6);
    self.unite(6, 7);
    self.unite(8, 9);
    self.unite(9, 4);
    self.unite(3, 9);
    

    
//    for(int i = 0;i < 8;i++)vec.push(i*111%50);
//    for(int i = 0;i < 8;i++)vec.pop();
//    vec.top() = 100;
//    st.push(10);
//    for(int i = 0;i < 8;i++)self.push_back(i*111%79);
//    QuickSort(self, 0, (int)self.size() - 1);
//    for(int i = 0;i < 3;i++)self.pop_back();
//    auto it = self.begin();
//    for(int i = 0;i < 3;i++)self.insert(it++, i);
//    for(int i = 0;i < 3;i++)self.erase(it--);
//    for(int i = 0;i < 3;i++)self[i] = i;
//    self.clear();
    return 0;
}

void QuickSort(visual_vector<int> & vec,int left,int right){
    if(right <= left)return;
    int key = vec[left], i = left, j = right + 1;
    while(1){
        while(vec[++i] <= key)if(i == right)break;
        while(vec[--j] >= key)if(j == left)break;
        if(i >= j)break;
        vec.swap(i, j);
    }
    vec.swap(j, left);
    QuickSort(vec, left, j-1);
    QuickSort(vec, j+1, right);
}

