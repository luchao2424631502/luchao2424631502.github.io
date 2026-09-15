---
title: STL中forwardlist的大致实现
date: '2021-09-15 18:13:00'
permalink: 2021/09/15/STL中forwardlist的大致实现/
categories:
- C++
tags:
- C++ STL
---

## STL中forward-list大致实现

### 1.`std::array<_Tp,std::size_t>`

> 源代码仔细看一下就知道了:`/usr/include/c++/9/array`

挑出来的大致实现:

> 主要的就是和traits(编译期传递类型)的配合,
>
> 可以看到std::array的内存分配就是在栈上的,没有使用分配器std::allocator,
>
> 对个数0特化

```cpp
#include <iostream>
#include <array>

#include <ext/aligned_buffer.h>
#include <bits/alloc_traits.h>
#include <bits/allocator.h>

/*
 * std::array<_Tp,std::size_t>的大致实现(g++9.3)
 * */
namespace llc
{
  template<typename _Tp,std::size_t _Nm>
    struct __array_traits
    {
      //数组类型
      typedef _Tp _Type[_Nm];
    };

  //偏特化
  template<typename _Tp>
    struct __array_traits<_Tp,0>
    {
      struct _Type {};
    };

  template<typename _Tp,std::size_t _Nm>
    struct array
    {
      typedef _Tp value_type;
      typedef value_type* pointer;
      typedef value_type& reference;
      typedef const value_type* const_pointer;
      typedef const value_type& const_reference;
      typedef value_type* iterator;
      typedef const value_type* const_iterator;
      typedef std::size_t size_type;
      typedef std::ptrdiff_t difference_type;
      //std::reverse_iterator<>是已经包装好的类,将普通iterator传入就行
      typedef std::reverse_iterator<iterator> reverse_iterator;
      typedef std::reverse_iterator<const_iterator> const_reverse_iterator;

      typedef __array_traits<_Tp,_Nm> _AT_Type;

      //template-class:data
      typename _AT_Type::_Type _M_elems;

      //接下来是function,和迭代器操作
    };
}

int main()
{
  std::array<int,10> ar1;
  std::cout <<  "int-size: " << sizeof(int) << " std::array-size " << sizeof(ar1) << "\n";
  /*
  llc::forward_list<int> f1;
  std::cout << "forward-list: " << sizeof(f1) << " pointer-size " << sizeof(int*) <<"\n";

  llc2::forward_list<int> f2;
  std::cout << sizeof(f2);
  */
}
```

### 2.`std::forward_list<_Tp,_Alloc>`

#### 1. gcc4.9的实现是从视频看到的

![1](/images/forward4.png)

#### 2.gcc9.3的实现是看源代码的

> 看起来大致结构是一样的

![2](/images/forward9.jpg)

#### 抽出来的源代码,解释在注释部分

```cpp
#include <iostream>
#include <array>

#include <ext/aligned_buffer.h>
#include <bits/alloc_traits.h>
#include <bits/allocator.h>

/*
 * forward-list的大致实现,(g++4.9 2014)
 * */
namespace llc
{
  //链表节点的父类:包含一个指向自己的指针
  template<typename _TP>
    struct _Fwd_list_node_base 
    {
      _Fwd_list_node_base *_M_next;
    };
  //链表的节点
  template<typename _Tp>
    struct _Fwd_list_node:public _Fwd_list_node_base<_Tp>
    {
      _Tp M_value;
    };

  //forward-list的代理实现类:包含了一个含指针的_Fwd_list_node_base类
  template<typename _Tp>
    struct _Fwd_list_impl:public std::allocator<_Fwd_list_node<_Tp>>
    {
      _Fwd_list_node_base<_Tp> _M_head;//一个指针
    };

  //forward-list的基类:包含一个forward-list的代理实现类
  template<typename _Tp>
    struct _Fwd_list_base
    {
      _Fwd_list_impl<_Tp> _M_impl;
    };

  //forward-list类:以private方式继承(不继承接口,继承的是数据成员(也就是实现))
  template<typename _Tp>
    struct forward_list:private _Fwd_list_base<_Tp>
    {
      //一系列接口函数
    };
}

/*
 * forward-list大致实现（g++9.3 2019)
 * */
namespace llc2
{
  struct _Fwd_list_node_base 
  {
    //构造函数
    _Fwd_list_node_base *_M_next = nullptr;
  };

  template<typename _Tp>
    struct _Fwd_list_node:public _Fwd_list_node_base 
    {
      //ext/aligned_buffer.h = __aligned_membuf<_Tp> = unsigned char _M_storage[sizeof(_Tp)];
      __gnu_cxx::__aligned_buffer<_Tp> _M_storage;
    };
  template<typename _Tp>
    struct _Fwd_list_iterator
    {
      typedef _Fwd_list_iterator<_Tp> _Self;
      typedef _Fwd_list_node<_Tp> _Node;

      typedef _Tp value_type;
      typedef _Tp* pointer;
      typedef _Tp& reference;
      typedef std::ptrdiff_t difference_type;
      typedef std::forward_iterator_tag iterator_category;
      //一系列函数
      _Fwd_list_node_base *_M_node;
    };

  template<typename _Tp>
    struct _Fwd_list_const_iterator
    {
      typedef _Fwd_list_const_iterator<_Tp> _Self;
      typedef const _Fwd_list_node<_Tp> _Node;
      typedef _Fwd_list_iterator<_Tp> iterator;

      typedef _Tp value_type;
      typedef const _Tp* pointer;
      typedef const _Tp& reference;
      typedef std::ptrdiff_t difference_type;
      typedef std::forward_iterator_tag iterator_category;

      //一系列函数
      const _Fwd_list_node_base* _M_node;
    };
  template<typename _Tp,typename _Alloc>
    struct _Fwd_list_base 
    {
      protected:
        /* bits/alloc_traits.h line 74中 __allocator_traits_base中Alloc::template rebind<_Fwd_list_node<_Tp>>::other;
         * bits/allocator.h line 124中std::allocator<_Tp>中 
         * template<typename _Tp1>
         * struct rebind { typedef allocator<_Tp1> other; };
         * 所以_Node_alloc_type等价与std::allocator<_Fwd_list_node<_Tp>>
         */
        typedef std::__alloc_rebind<_Alloc,_Fwd_list_node<_Tp>> _Node_alloc_type;
        //alloc_traits
        typedef __gnu_cxx::__alloc_traits<_Node_alloc_type> _Node_alloc_traits;
        

        /*Alloc::other看名字像std::allocator中的一个类型,推测_Fwd_list_impl还是继承了std::allocator的接口
         * 和gcc4.9比起来好相似,都是继承std::allocator
         */
        struct _Fwd_list_impl:public _Node_alloc_type
        {
          //成员变量,_M_head是一个指针
          _Fwd_list_node_base _M_head;
          //其它的是构造函数
        }; 

        /*_Fwd_list_base的成员变量是_Fwd_list_impl,看来forward-list的基类的实现方式
         * 还是通过代理给impl类实现*/
        _Fwd_list_impl _M_impl;
      public:
        typedef _Fwd_list_iterator<_Tp> iterator;
        typedef _Fwd_list_const_iterator<_Tp> const_iterator;
        typedef _Fwd_list_node<_Tp> _Node;

        //下面是一些函数
    };

  //正式的forward-list容器来了,private方式继承_Fwd_list_base,也就是包含了实现
  template<typename _Tp,typename _Alloc=std::allocator<_Tp>>
    class forward_list:private _Fwd_list_base<_Tp,_Alloc>
    {
      private:
        typedef _Fwd_list_base<_Tp,_Alloc> _Base;//父类类型
        typedef _Fwd_list_node_base _Node_base;//节点类的父类类型
        //等价与= typedef _Fwd_list_node<_Tp> _Node;
        typedef typename _Base::_Node _Node;
        //等价与= typedef std::__alloc_rebind<_Alloc,_Fwd_list_node<_Tp>> _Node_alloc_type;
        typedef typename _Base::_Node_alloc_type _Node_alloc_type;
        //traits 和上面的一样都来自 _Fwd_list_base类
        typedef typename _Base::_Node_alloc_traits _Node_alloc_traits;
        //_Tp分配器的traits
        typedef std::allocator_traits<std::__alloc_rebind<_Alloc,_Tp>> _Alloc_traits;

      public:
        //下面是给traits用的
        typedef _Tp value_type;
        //_Alloc_traits是_Tp的traits
        typedef typename _Alloc_traits::pointer pointer;
        typedef typename _Alloc_traits::const_pointer const_pointer; 
        typedef value_type& reference;
        typedef const value_type& const_reference;

        typedef typename _Base::iterator iterator;
        typedef typename _Base::const_iterator const_iterator;
        typedef std::size_t size_type;
        typedef std::ptrdiff_t difference_type;
        typedef _Alloc allocator_type;
      //下面的全是forward-list的接口
    };
}

int main()
{
  llc::forward_list<int> f1;
  std::cout << "forward-list: " << sizeof(f1) << " pointer-size " << sizeof(int*) <<"\n";

  llc2::forward_list<int> f2;
  std::cout << sizeof(f2);
}
```
