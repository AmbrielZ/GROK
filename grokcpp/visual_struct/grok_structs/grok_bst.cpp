
//
//  main.cpp
//  BinarySearchTree
//
//  Created by 胡泽弘 on 2022/6/2.
//

#include <iostream>
#include <vector>
#include "../grok_base.hpp"
using namespace std;

template<class _Tp>
class grok_BST{
public:
    grok_base::msg _hrm;
    grok_BST(string type = "Bst"):root(NULL),_size(0),_hrm(new grok_base::head())
    { delete _hrm.sendto((new grok_base::act(1,0))->push(type));}
    ~grok_BST(){delete _hrm.sendto((new grok_base::act(-1,0)));}
    
    bool insert(_Tp x){
        if(find(x))return 0;
        delete _hrm.sendto((new grok_base::act(5,1))->push(x));
        grok_TreeNode * p = root;
        while(p && p->val != x){
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
        if(!root)root = new grok_TreeNode(x);
        return ++_size;
    }
    bool erase(_Tp x){
        if(!find(x))return 0;
        delete _hrm.sendto((new grok_base::act(6,1))->push(x));
        grok_TreeNode * p = root;
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
        else root = r;
        _size--;
        return 1;
    }
    _Tp successor(int x){
        grok_TreeNode * p = root;
        grok_TreeNode * q = NULL;
        while(p && p->val != x){
            if(p->val > x){
                q = p;
                p = p->left;
            }
            else p = p->right;
        }
        if(p && p->right)return minimu(p->right);
        else return q->val;
    }
    _Tp predessor(int x){
        grok_TreeNode * p = root;
        grok_TreeNode * q = NULL;
        while(p && p->val != x){
            if(p->val < x){
                q = p;
                p = p->right;
            }
            else p = p->left;
        }
        if(p && p->left)return maximu(p->left);
        else return q->val;
    }
    _Tp maximu(grok_TreeNode * p){
        if(!p)return NULL;
        while(p->right)p = p->right;
        return p->val;
    }
    _Tp minimu(grok_TreeNode * p){
        if(!p)return NULL;
        while(p->left)p = p->left;
        return p->val;
    }

    bool ismember(int x){
        return find(x);
    }
    
    size_t size(){
        return _size;
    }
//protected:
    
    grok_TreeNode * find(int x){
        grok_TreeNode * p = root;
        while(p && p->val != x){
            if(p->val > x)p = p->left;
            else p = p->right;
        }
        return p;
    }
    grok_TreeNode * root;
    int _size;
};


void inorder(grok_TreeNode * p,vector<grok_TreeNode *> & vec,int i){
    if(p->left){
        inorder(p->left, vec, i);
        vec[i + p->left->size] = p;
    }
    else vec[i] = p;
    if(p->right)inorder(p->right, vec, i + p->size - p->right->size);
}

