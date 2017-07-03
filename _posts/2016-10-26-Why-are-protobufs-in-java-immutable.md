---
layout: post
title: Immutability of protobufs - Java vs C++
comments: true
summary: "Why are protobufs in Java are immutable while their cpp counter parts are not"
tags: ['c++', 'java', 'tech' ]
---

[Protocol buffers](https://developers.google.com/protocol-buffers/) (aka protobufs, protos) are a language-neutral, platform-neutral 
extensible mechanism for serializing structured data. 

###**C++ const keyword**
C++ does not need immutable protobufs - the `const` keyword is the reason.
If an object is passed to a function as a const, only the methods which are marked as const can be accessed. See the below example.

```C++
class Boo {
 public:
  void set_val(int nval) { val = nval; }
  int get_val() const { return val; }

 private:
  int val;
};

void function(const Boo& b1, Boo& b2) {
  // The below statement produces compile a error for accessing non
  // const function of a const param. All the other statements are fine.
  b1.set_val(0); 
  b1.get_val();
  b2.set_val(0);
  b2.set_val();
}
```

###**Why are protobufs in Java are immutable**
Java has no equivalent of C++ `const`. If a function takes in a mutable object,
just by looking at the function definition, one cannot say whether it is 
modifying the object or not. So in Java it is preferred to make objects
immutable as much as possible. This is not a problem in C++ because of the `const` keyword. 

For every proto message definition, the Java protobuf library creates an
immutable protobuf class and a mutable builder class.

### Conclusion

- Intent to **modify**
  - C++  : protobuf is passed (not as a  const)
  - Java : a protobuf builder object is passed
- Intent to **read** 
  - C++  : protobuf is passed  as a const
  - Java : a protobuf object (immutable) is passed

**Some Realization**  
I'm finding it extremely hard to `search` for the right topics and write something reasonably long and 
meaningful. Instead I decided to write about short and `seemingly` obvious things.
