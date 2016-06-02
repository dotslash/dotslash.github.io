---
layout: post
title: "Expiring records : Redis ttl, guava cache"
tags: ['tech']
comments: true
summary: "How do redis ttls and guava cache expiring records work"
---
In my recent job interviews, I was asked a few times about how to expire stale data in various scenarios (and I gave acceptable solutions). This made me want to know how this is done in practice. I read (docs/code) of how Redis implements ttl (time to live) and how Guava cache does record expiry.

**Note** : In this post Im just writing **how** Redis and guava are doing this and **not about the pros and cons** of the approaches chosen. I would love to go into the details, but not in this post. (Feel free to offer suggestions on that front)

- [Redis](https://redis.io) is an in-memory key value store, which can logically be seen as huge hash table  
- [Guava Cache](https://github.com/google/guava/wiki/CachesExplained) is a caching utility (part of the guava library). Internally this also is a hash map  

## Formalizing the problem
Implement a hash based data structure, which supports record expiry. The expiry policies be one of the following

- Record Level expiry
- Records expire based on idle time (not queried/modified for x secs)
- LRU cache with fixed number of entries

## Hash table basics
Most of the hash table implementations are just arrays of linked lists. The linked list at `hashcode(key) % array_size`th index in the array will contain the data for the value of `key`. So the node for the linked list will look something like this

```
Node
 - key       
 - data       : value
 - list_next  : pointer to next Node in linked list
 - extra_data : other extra data based on exact use case
```

## LRU Cache

This can be done without any extra threading as we expire entries only when data is added (if we are out of space). One way to implement this is to maintain a doubly linked list in extra_data which is ordered by access/write times. If we stick to general template for Hash Entry, this is how the extra data looks like to support this.

```
extra_data : contains information to maintain the Lru linked list
 - lru_next : pointer to next Node in lru linked list
 - lru_prev : pointer to previous node in lru linked list
```
When an entry is accessed/edited then the Node is added to the end of lru linked list and is removed from its original position. Note that this does not have to interfere at all with the original hash data structure.

Redis has an option of maintaining an LRU cache. But it is approximate. It maintains pool of good candidates for eviction. Every time when the limit is reached, it fetches a random sample of keys and updates its eviction pool with better candidates from this sample. Then it simply deletes the most stale entry from the pool. What Redis gains by doing this is, it does not need the lru linked list (smaller memory footprint).

Redis source corresponding to this :  [dictGetSomeKeys](https://github.com/antirez/redis/blob/b5352eea51f2881d13ec4e3e1fa90cea037d4f29/src/dict.c#L689),
[evictionPoolPopulate](https://github.com/antirez/redis/blob/9200312ab64d65a908709dc5dfb0dd1431733b21/src/server.c#L3403),
[freeMemoryIfNeeded](https://github.com/antirez/redis/blob/9200312ab64d65a908709dc5dfb0dd1431733b21/src/server.c#L3468)

## Record level expiry : Redis

In Redis each key can have its own expiry set. Redis maintains in another hash table (`expires` table) the keys and their corresponding expiry times. It has a periodic task which removes expired entries. This task picks 20 random elements in this `expires` table and deletes the expired elements. A single invocation of this task keeps repeating until < 25% of the sample need to removed.

But this does not guarantee that all expired entries are removed. So every read operation will check if the element being accessed is stale or not and removes it if the entry is stale.

Corresponding redis source code : [expireIfNeeded](https://github.com/antirez/redis/blob/646c958bbd506839f02dbe8801275e11e2657955/src/db.c#L933),
[activeExpireCycle](https://github.com/antirez/redis/blob/9200312ab64d65a908709dc5dfb0dd1431733b21/src/server.c#L794)

## Expire based on idle time

An approach very similar to the LRU cache implementation would work here. We can have a cleanup task whenever a read/write call is made. Along with this we also need to maintain and update last accessed time. Guava cache does something very similar.

Corresponding guava source code  : [get](https://github.com/google/guava/blob/5b608043b9d56a4427a2d8c1583f6f3c5a4e1023/guava/src/com/google/common/cache/LocalCache.java#L2791), [getLiveValue](https://github.com/google/guava/blob/5b608043b9d56a4427a2d8c1583f6f3c5a4e1023/guava/src/com/google/common/cache/LocalCache.java#L2772), [expireEntries](https://github.com/google/guava/blob/5b608043b9d56a4427a2d8c1583f6f3c5a4e1023/guava/src/com/google/common/cache/LocalCache.java#L2651)

## Closing remarks

LRU can be made to work with a single thread. For record level expiry, I cannot think of a single threaded approach as a scheduled cleanup task seems necessary. The same applies to idle time based expiry (unless we want to expire records lazily).
