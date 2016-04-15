def hanoi(n, fr, to, buf):
    if (n == 0):
        return
    #print "deb", 'l', n, fr, to, buf
    hanoi(n-1, fr, buf, to)
    #print "deb", 'r', n, fr, to, buf
    print "{} {}->{}".format(n, fr, to)
    hanoi(n-1, buf, to, fr)

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

def selectK_iter(inp, k):
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


print "hanoi size=3"
hanoi(3, 1, 2, 3)
print "hanoi iter size=3"
hanoi_iter(3, 1, 2, 3)
print "========"
print "selectK n=4, k=2"
print '\n'.join(map(str, selectK(range(4), 2)))
print "selectK iter n=4, k=2"
print '\n'.join(map(str, selectK_iter(range(4), 2)))
