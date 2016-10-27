---
layout: post
title: Protobufs immutability - java , cpp?
comments: true
summary: "Why are protobufs in java are immutable while their cpp counter parts are not"
tags: ['c++', 'java', 'tech' ]
---

###**C++ const keyword**
The `const` keyword in c++ is the reason why it does not need immutable 
[protocol buffers](https://developers.google.com/protocol-buffers/). If an object is passed to a function as a const, 
only the methods which are marked as const can be accessed. See the below example.

```c++
class Boo {
 public:
  void set_val(int nval) { val = nval; }
  int get_val() const { return val; }

 private:
  int val;
};

void function(const Boo& b1, Boo& b2) {
  // The below statement produces compile error for accessing non
  // const function of a const param. All the other statements are fine.
  b1.set_val(0); 
  b1.get_val();
  b2.set_val(0);
  b2.set_val();
}

```
###**Why are protobufs in java are immutable**
It is a common pattern in c++ to declare a parameter as a `const` if the function has no intent to modify it.
Java has no equivalent feature. So the work-around was to make all protobufs immutable.
So if a function is accepting a protobuf in java, it means it has no intent to modify the protobuf object. 

It is a standard use case to initialize a protobuf and pass it multiple functions which each function sets some
attributes of the object. For this use case, in c++ the function would accept a non const reference to protobuf, in java
the function would accept the protobuf's associated builder.

**Some Realization**  
Im finding it extremely hard to `search` for the right topics and write something reasonably long and meaningful.
Instead I decided to write about short and `seemingly` obvious things.
