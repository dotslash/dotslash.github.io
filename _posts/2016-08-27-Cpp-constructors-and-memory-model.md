---
layout: post
title: C++ copies and Memory model
comments: true
summary: "C++ constructors and Memory model"
tags: ['c++', 'tech']
---
###Some seemingly simple operations
Take a look at the below class declaration and the 3 statements below.

```c++
class MyType {
  int a; // 4 bytes
  int b; // 4 bytes
  AnotherType c; // lets say 20 bytes
};

///
MyType obj1;  // Statement 1
MyType obj2 = obj1; // Statement 2
obj2 = obj1; // Statement 3
```
If you are java programmer you would consider the 3 statements trivial and the
only thing you would possibly be worried about is obj1 is not initialized.

But in c++, that is not the case. In java pointers are hidden (you only hold
references or primitives). In c++, by default you create objects in the [stack](https://en.wikipedia.org/wiki/Call_stack).

So in the above code, `Statement 1` would allocate 28 bytes of memory on the
stack for obj1 and call the default constructor.

`Statement 2` would allocate 28 bytes of memory and call the copy constructor on
obj2 and `Statement 3` would call copy assignment constructor on obj2. Details on
copy and copy assignment constructor are explained later. But by now I hope
I made it clear that these statements are not as innocent as they seem to be.

###Copy [assignment]? constructor
By default every class has a Copy and Copy Assignment constructor (unless they
are explicitly/implicitly deleted).

A Copy constructor is invoked on an object if the object is initialized with the intent to copy (as in `Statement 2`)

A Copy assignment constructor is invoked on an object if the object is already
initialized and is now being copied from another object (as in `Statement 3`).
Here before the copy  happens, the resources being held by the object need to
be released  appropriately. E.g A copy assignment an string would possibly
involve releasing the the char[] it holds, allocating memory for a new char[]
from the heap and copy the data[?].

**Note**: c++ 11 introduced move semantics and this brought in move constructor and
move assignment constructor. To understand this one needs to understand rvalues
and lvalues. While I (think) I know these concepts fairly well, my
understanding is not enough to give a simple explanation about them.

###Memory Model
Any single threaded program's state can be represented using what's on the stack and
what's on the heap. Heap is where all the dynamically allocated memory is
stored. Stack is the function call stack. 

<img src="/public/images/program-memory.jpg"/>
Take a look at the below program. We will see how the stack and heap will look like at `Marker`

```c++
void func() {
  MyType o1;
  MyType o2;
  MyType* p1 = new MyType(); // Memory Leak
  MyType* p2 = new MyType();
  // ---Marker---
  delete p2;
}

int main(int argc, char** argv) {
  MyType m1;
  func();
}
```

When the program's execution is at `Marker` (before the delete statement), our
stack and heap are as follows.

- 

