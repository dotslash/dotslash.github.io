---
layout: post
title: Converting any recursion to stack
tags: ['tech']
comments: true
summary: "Converting any recursion to stack; Tower of hanoi, N choose K problems"
---
I've seen a couple of blogs which talk about this, but most of them have very simple examples. I will go with non trivial ones and my solutions will mimic the function call stack.

Lets start with a simple example, the [Tower of Hanoi](https://en.wikipedia.org/wiki/Tower_of_Hanoi) problem.

###Tower of Hanoi
>The Tower of Hanoi (also called the Tower of Brahma or Lucas' Tower) is a mathematical game or puzzle. It consists of three rods, and a number of disks of different sizes which can slide onto any rod. The puzzle starts with the disks in a neat stack in ascending order of size on one rod, the smallest at the top, thus making a conical shape.

>The objective of the puzzle is to move the entire stack to another rod, obeying the following simple rules:
>
> - Only one disk can be moved at a time.
> - Each move consists of taking the upper disk from one of the stacks and placing it on top of another stack i.e. a disk can only be moved if it is the uppermost disk on a stack.
> - No disk may be placed on top of a smaller disk.
>
> [Tower of Hanoi wikipedia](https://en.wikipedia.org/wiki/Tower_of_Hanoi)

The below code contains both the recursive and iterative solution. The tricky part is there are 2 recursive calls in the function. If there is only one recursive call it would be straight forward using a simple while loop.

``` python
def hanoi(n, fr, to, buf):
    if (n == 0):
        return
    #print "deb", 'l', n, fr, to, buf
    hanoi(n-1, fr, buf, to)
    #print "deb", 'r', n, fr, to, buf
    print "{} {}->{}".format(n, fr, to)
    hanoi(n-1, buf, to, fr)
```
Now lets think of how the compiler deals with stack. Before the first call to hanoi, it saves the state of the function's execution, in the call stack's present entry, pushes a new entry to the stack for recursive call and starts executing the operations in recursive call. Lets do the same thing

```python
def hanoi_iter(n, fr, to, buf):
    stack = list() #python's list can be used as stack
    stack.append(('full', n, fr, to, buf))
    while len(stack) != 0:
        op, n, fr, to, buf = stack.pop()
        if n == 0:
            continue
        #print "deb", op, n, fr, to, buf
        if op == 'step1':
            print "{} {}->{}".format(n, fr, to)
            stack.append(('full', n-1, buf, to, fr))
        else:
            #saving the state
            stack.append(('step1', n, fr, to, buf))
            stack.append(('full', n-1, fr, buf, to))
```
I'm differentiating between saved state(`step1`) and full function call(`full`) by the first value (lets call it operation) in stack entries. Until the stack becomes empty, we pop an entry from stack, handle the base cases, then work based on the operation.

For saved state, print the move and then do full call on smaller problem. For the full case, we save the state and mark the state as `'step1'`, and then do the full call on sub problem. That does the job.

This formulation works as long as the functions have no return value. The N Choose K problem will tackle that.
###N Choose K
Given a list of elements, return all possible ways of picking K elements as a list of lists. There are 6 ways picking 2 elements from `[0,1,2,3]` `[0,1] [0,2] [0,3] [1,2] [1,3] [2,3]`

One recursive solution for this is to

- Pick the list's first element and pick k-1 elements from sublist from 1 to end
- Do not pick the first element of list and pick k elements from sublist from 1 to end
- Return the union of both

The below code implements that

```python
def selectK(inp, k, start=0, to_add=[]):
    if (len(inp) - start) < k or k < 0:
        #invalid
        return []
    if k == 0:
        #one way to pick no elements; pick nothing; but add to_add
        return [list(to_add)]
    if (len(inp) - start) == k:
        #only k present in the array, pick them all; add to_add
        ret = list(to_add)
        ret.extend(inp[start:])
        return [ret]
    #Base cases done
    #pick k elements in inp[start+1:] and not include inp[start]
    without_pres = selectK(inp, k, start+1, to_add)

    #step1(of stack solution) starts here
    #pick k-1 elements in inp[start+1:] and include inp[start]
    to_add.append(inp[start])
    with_pres = selectK(inp, k-1, start+1, to_add)

    #step2(of stack solution) starts here
    to_add.pop()
    ret = with_pres
    ret.extend(without_pres)
    return ret
```
Here we have 2 recursive calls and we need results of both of them to compute the final result. (In the previous problem we did not need the return value at all) So we split the function to 3 (as opposed to 2 for Hanoi). I marked them as `'full'` , `'step1'`, `'step2'`

The main problem is passing the return value. If we go back to how compiler does call stacks, its just a stack and one a stack is popped then its output is determined and passed to the caller's stack. So we need exactly one variable which can pass the return variable between caller and callee.

```python
def selectK_rec(inp, k):
    stack = list()
    # 5 elements in the tuple
    # (operation, k, start_of_list, to_add, extra_info)
    stack.append(('full', k, 0, [], None))
    ret = None
    while len(stack) != 0:
        opn, k, start, to_add, extra = stack.pop()
        if opn == 'full':
            #base cases; replace returns in recursive version
            #with assignments to tmp
            if (len(inp) - start) < k or k < 0:
                #invalid
                ret = []
                continue
            if k == 0:
                #one way to pick no elements;
                #pick nothing; but add to_add
                ret = [list(to_add)]
                continue
            if (len(inp) - start) == k:
                #only k present in the array,
                #pick them all; add to_add
                ret = list(to_add)
                ret.extend(inp[start:])
                ret = [ret]
                continue
            #base cases Done
            #save the state
            stack.append(('step1', k, start, to_add, None))
            stack.append(('full', k, start+1, to_add, None))
        elif opn == 'step1':
            to_add.append(inp[start])
            stack.append(('step2', k, start, to_add, ret))
            stack.append(('full', k-1, start+1, to_add, None))
        else:
            to_add.pop()
            with_pres = ret
            without_pres = extra
            with_pres.extend(without_pres)
            ret = with_pres
    return ret
```
I initialize the `ret` var to None. Wherever in the recursive code, I returned a value, in the stack solution I assign that value to `ret`. Finally return the same variable.

With this approach any recursive code can be converted to stack based iteration. I shared the [full code with examples](https://gist.github.com/dotslash/8fb472cd9fa22d9f126b57d5e2e17c9c) as a gist
