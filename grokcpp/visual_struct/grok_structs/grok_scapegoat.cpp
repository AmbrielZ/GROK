//
//  grok_scapegoat.cpp
//  overload.cpp
//
//  Created by 胡泽弘 on 2022/11/28.
//

#include "grok_bst.cpp"
using namespace std;

template<class _Tp>
class grok_scapegoat:public grok_BST<_Tp>{
public:
    grok_scapegoat(double x = 0.7):alpha(x), grok_BST<_Tp>("scapegoat"){}
    grok_TreeNode * find(_Tp x){
        string tracker;
        grok_TreeNode * p = grok_BST<_Tp>::root;
        grok_TreeNode * q = NULL;
        while(p && p->val != x){
            if(p->unbalanced(alpha)){
                vector<grok_TreeNode *> vec(p->size);
                inorder(p, vec, 0);
                p = buildtree(vec, 0, p->size-1);
                if(q){
                    if(x < q->val)q->left = p;
                    else q->right = p;
                }
                else grok_BST<_Tp>::root = p;
                delete this->_hrm.sendto((new grok_base::act(9,1))->push(tracker));
            }
            q = p;
            tracker += '0' + (x > p->val);
            if(x > p->val)p = p->right;
            else p = p->left;
        }
        return p;
    }
    
    bool insert(_Tp x){
        if(find(x))return 0;
        delete this->_hrm.sendto((new grok_base::act(5,1))->push(x));
        grok_TreeNode * p = grok_BST<_Tp>::root;
        while(p){
            p->size++;
            if(p->val > x){
                if(p->left)p = p->left;
                else{
                    p->left = new grok_TreeNode(x);
                    break;
                }
            }
            else{
                if(p->right)p = p->right;
                else{
                    p->right = new grok_TreeNode(x);
                    break;
                }
            }
        }
        if(!grok_BST<_Tp>::root)grok_BST<_Tp>::root = new grok_TreeNode(x);
        return 1;
    }
    
    void erase(_Tp x){
        if(!find(x))return;
        delete this->_hrm.sendto((new grok_base::act(6,1))->push(x));
        grok_TreeNode * p = grok_BST<_Tp>::root;
        grok_TreeNode * q = NULL;
        while(p->val != x){
            p->size--;
            q = p;
            if(p->val > x)p = p->left;
            else p = p->right;
        }
        if(p->left && p->right){
            grok_TreeNode * r = p;
            p->size--;
            q = p;
            p = p->left;
            while(p->right){
                p->size--;
                q = p;
                p = p->right;
            }
            r->val = p->val;
            x = r->val;
        }
        grok_TreeNode * r = p->left ? p->left : p->right;
        if(q){
            if(x > q->val)q->right = r;
            else q->left = r;
        }
        else grok_BST<_Tp>::root = r;
    }
    
    size_t size(){
        return grok_BST<_Tp>::root ? grok_BST<_Tp>::root->size : 0;
    }
    
private:
    double alpha;
    grok_TreeNode * buildtree(vector<grok_TreeNode *> & vec,int left,int right){
        if(left > right)return NULL;
        int mid = (left+right)>>1;
        grok_TreeNode * p = vec[mid];
        p->left = buildtree(vec, left, mid-1);
        p->right = buildtree(vec, mid+1, right);
        p->resize();
        return p;
    }
    void inorder(grok_TreeNode * p,vector<grok_TreeNode *> & vec,int i){
        if(p->left){
            inorder(p->left, vec, i);
            vec[i + p->left->size] = p;
        }
        else vec[i] = p;
        if(p->right)inorder(p->right, vec, i + p->size - p->right->size);
    }
};
