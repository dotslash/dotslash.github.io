---
layout: post
title: Simple Graph Traversals with Redis UDFs
tags: ['redis', 'tech']
comments: true
summary: "Playing around with lua udfs on redis for simple graph traversals"
---

While i was trying to think various approaches on some ‘work’ related projects, this suddenly occurred to me that, For simple graph traversals with edges stored in some DB, a db-server side UDF (User defined function) would be very efficient. In my work place we use [aerospike](http://aerospike.com) a lot and that made me ask this question in aerospike forums forums ([graph-traversal-using-udf](https://discuss.aerospike.com/t/graph-traversal-using-udf/2127)). Then I started looking if something like this is possible with [redis](http://redis.io) (which aerospike primarily tries to replace) and they do.

Essentially what we need is the the UDF api being able to make db requests. From what I understand as of now aerospike does not allow that. So I decided to do some basic experiment about this on redis. Theoretically this should bring a significant performance gain as most of the time is spent on the network IO (redis server side latency will be minimal as all the data is stored in memory).

## Background on Redis UDFs

Redis supports UDFs in [lua](http://www.lua.org/) language. For detail more details checkout [lua](http://lua.org) website and [redis UDF docs](http://redis.io/commands/eval). To reproduce my experiment, the only requirements are loading lua scripts to redis server and invoking the UDF from the python client. The below command loads the udf to redis.

```
redis-cli script load "$(cat ~/find_parent.lua)"
# this loads the lua script in 'find_parent.lua' to redis
# the output for redis outputs 'SHA1 digest of the script
# 9e4c3550b2961d085916ecdead255cde6b450f6b in my case
# http://redis.io/commands/script-load
```

## Problem Statement

All the edges of a graph are stored, in a redis db. The graph is a [forest](https://en.wikipedia.org/wiki/Tree_(graph_theory)#forest) ( a bunch of trees). Given a node, the goal is to find the root of the tree the input node belongs to.

## Generating the graph edges

I wrote the below simple program which populates a forest in redis.

```python
# first arg is to set the group size
# example : if group size = 10
# there will be edges between
# 0-1,1-2,2-3,..8-9 : this tree is rooted at 0
# 10-11, 11-12, ... 18-19 : this tree is rooted at 10
import redis
import sys
tot = 1000
split = int(sys.argv[1])
if tot % split != 0 :
    print "first param should divide 1000 perfectly";
    sys.exit(1)
rows = tot/split
cols = split
rc = redis.StrictRedis(host='127.0.0.1')
for i in xrange(rows):
    rc.delete(i*cols)
    for j in xrange(1, cols):
        rc.set(i*cols + j, i*cols + j - 1)
```
## Standard Approach

The standard approach would be to get parent node in redis until a node is reached which does not have a parent

```python
import redis
import time
import sys
tc = int(sys.argv[1])
rc = redis.StrictRedis(host='127.0.0.1')
def get_root(val):
    limit = 100
    while limit &gt; 0:
        pres = rc.get(val)
        if pres == None : return val
        val = pres
        limit -= 1
    return val
start = time.time()
print "start", start
for i in xrange(tc):
    get_root(str(i%1000))

end = time.time()
print "end  ", end
print end-start
```


## Lua Udf

I wrote the a lua script which does exactly what my get_root function does in the python code in the previous section

```lua
--9e4c3550b2961d085916ecdead255cde6b450f6b;
local ret = KEYS[1]
local limit = 100
while limit ~= 0 do
    local pres = redis.pcall("GET", ret)
    if pres == nil or type(pres) == "boolean"; then return ret end
    ret = pres
    limit = limit - 1
end
return ret
```

This is updated python code to use the UDF

```python
import redis
import time
import sys
tc = int(sys.argv[1])
rc = redis.StrictRedis(host='127.0.0.1')
def get_root(val):
    return rc.evalsha("9e4c3550b2961d085916ecdead255cde6b450f6b", 1, val)
start = time.time()
print "start", start
for i in xrange(tc):
    get_root(str(i%1000))

end = time.time()
print "end  ", end
print end-start
```
## Results

Here are the results in secs. First column has the size of each group (groupsize/2 will be the expected number of traversals). The 2nd and 3rd columns show the time taken for 10K requests (see problem statement) without and with udf

```
groupsize  without_udf  with_udf
==================================
5          1.39         0.58
10         2.72         0.61
20         5.00         0.75
50         13.64        0.72
100        24.98        0.82
1          0.45         0.57
```

When every node in itself is a tree (last row), we can observe the extra cost it takes to execute the ‘udf’. But in general when the expected number of traversals keep increasing performance with udf does not degrade while it (obviously) does in the other case, as more traversals means more DB calls (network IO). And this is the case when everything is happening on localhost. When the db is lying on different servers, the udf will be even more beneficial.

## Notes/Extra Reading

1.  All these make a lot of sense when the DB is not close to its full load capacity. If full capacity, it gets tricky, but I believe even in that case UDF can only make things better.
2.  Latency Numbers Every Programmer Should Know : [https://gist.github.com/jboner/2841832](https://gist.github.com/jboner/2841832)
3.  Source code : [https://gist.github.com/dotslash/5238a225072d2e74627c](https://gist.github.com/dotslash/5238a225072d2e74627c)
4.  One downside of this is debugging is really painful and documentation redis has for UDF is pretty poor (IMHO) or its only me (?). But before considering this, keep in mind that ‘Premature optimization is root of all evil’
5.  **UPDATE : Why aerospike does not support this**  
    “The UDF can operate on a single record in an invocation. Once its is invoked for a record, it cannot access other records. The basic reason why this is not allowed is that the record may be on a different node. We don’t want the UDF to do distributed transaction” – [https://discuss.aerospike.com/t/graph-traversal-using-udf/2127/2?u=yesteapea](https://discuss.aerospike.com/t/graph-traversal-using-udf/2127/2?u=yesteapea).  
    It will be interesting to see how well redis handles this when [partitioning](http://redis.io/topics/partitioning) is enabled
