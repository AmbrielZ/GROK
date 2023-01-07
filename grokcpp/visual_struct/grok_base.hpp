//
//  grok_base.hpp
//  overload.cpp
//
//  Created by 胡泽弘 on 2022/11/15.
//

#ifndef grok_base_hpp
#define grok_base_hpp

#include <stdio.h>
#include <iostream>
#include <fstream>
#include <vector>
#include <sstream>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <typeinfo>
//#include "msg.pb.h"

//默认 0为无值 1为单值/双值 2为多值 3为重复多值
//-1 over
//1 init
//2 change
//3 push_back unite
//4 pop_back
//5 insert
//6 erase
//7 swap
//8 clear
//9 rebuild

namespace grok_base{
using namespace std;
int g_count = 1;

#define _buf_ 128
class grok_udp{
public:
    grok_udp():__client_sock(socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)){
        __addr.sin_family = AF_INET;
        int server_port = 7851;
        __addr.sin_port = htons(server_port);
        char server_ip[16] = "127.0.0.1";
        __addr.sin_addr.s_addr = inet_addr(server_ip);
    }
    void sendto(const string & __msg_){
        sprintf(__msg_buf, "%s",__msg_.c_str());
        ::sendto(__client_sock, __msg_buf, strlen(__msg_buf), 0, (sockaddr*)(&__addr), sizeof(__addr));
        memset(__msg_buf, 0, _buf_);
    }
    int __client_sock;
    sockaddr_in __addr;
    char __msg_buf[_buf_];
};

grok_udp * __udp_ = new grok_udp();

class head{
public:
    head():gid(g_count++){}
    string put(){
        return to_string(gid);
    }
    int gid;
};

class act{
public:
    act(int _x,int _y = 0):type(_x),subtype(_y){}
    
    template<class _Tp>
     act * push(const _Tp & _tmp){
         stringstream ss;
         ss << ' ' << _tmp;
         datas += ss.str();
         return this;
    }
    
    template<class _Tp>
    act * push(const vector<_Tp> & vec){
        stringstream ss;
        for(auto & c : vec)ss << ' ' << c;
        datas += ss.str();
        return this;
    }
    
    string put(){
        stringstream ss;
        ss << type << ' ' << subtype;
        if(!datas.empty())ss << datas;
        return ss.str();
    }
    int type;
    int subtype;
    string datas;
};

class msg{
public:
    msg(head * _h = NULL):_head(_h){}
    head * _head;
    act * sendto(act * _act){
        cout << _head->put() << ' ' << _act->put() << endl;
        __udp_->sendto(_head->put() + ' ' + _act->put());
        return _act;
    }
};
};


class grok_TreeNode{
public:
    grok_TreeNode():val(0),left(NULL),right(NULL),size(1){}
    grok_TreeNode(double x):val(x),left(NULL),right(NULL),size(1){}
    grok_TreeNode(double x,grok_TreeNode * l):val(x),left(l),right(NULL),size(l ? l->size + 1: 1){}
    grok_TreeNode(double x,grok_TreeNode * l,grok_TreeNode * r):val(x),left(l),right(r),
    size(1+(l ? l->size : 0)+(r ? r->size : 0)){}
    //basic:
    grok_TreeNode * left;
    grok_TreeNode * right;
    double val;
    //augment:
    int size;
    //scapegoat
    bool unbalanced(double alpha){
        return (left && left->size > alpha*size) || (right && right->size > alpha*size);
    }
    void resize(){
        size = (left ? left->size : 0) + (right ? right->size : 0) + 1;
    }
};

void inoder(grok_TreeNode * p){
    if(p->left)inoder(p->left);
    std::cout<<p->val<<":"<<p->size<<" ";
    if(p->right)inoder(p->right);
}

#endif /* grok_base_hpp */

