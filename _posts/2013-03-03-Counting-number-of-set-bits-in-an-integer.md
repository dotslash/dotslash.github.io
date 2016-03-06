---
layout: post
title: Counting set bits in an integer
tags: ['c++', 'tech']
comments: true
summary: "Understanding the magic numbers in counting set bits in an integer/long"
---

Most natural ways to do this is to loop through all bits in the integer increment the count for each set bit.

```c++
int NumberOfSetBits(int n){
  int count = 0;
  while(n){
    count += n & 1;
    n >>= 1;
  }
  return count;
}
```

But we can do better. The following code works perfectly fine for counting the number of bits set.

```c++
//for 64 bit numbers
int NumberOfSetBits64(long long i)
{
    i = i - ((i >> 1) & 0x5555555555555555);
    i = (i & 0x3333333333333333) +
        ((i >> 2) & 0x3333333333333333);
    i = ((i + (i >> 4)) & 0x0F0F0F0F0F0F0F0F);
    return (i*(0x0101010101010101))>>56;
}
//for 32 bit integers
int NumberOfSetBits32(int i)
{
    i = i - ((i >> 1) & 0x55555555);
    i = (i & 0x33333333) + ((i >> 2) & 0x33333333);
    i = ((i + (i >> 4)) & 0x0F0F0F0F);
    return (i*(0x01010101))>>24;
}
```

The magic numbers might seem very confusing. But they are not random (obviously!).  
Let us start with 0X55555555\. Binary representation of 5 is 0101\. So 0X55555555 has 16 ones, 16 zeros and the ones,zeros take alternate positions. Similarly 0X33333333 has 16 ones, 16 zeros and 2 consecutive ones, 2 consecutive zeros alternate.

```c++
F = 0x55555555 = 01010101010101010101010101010101
T = 0x33333333 = 00110011001100110011001100110011
O = 0x0f0f0f0f = 00001111000011110000111100001111
```

Now split the number into 16 sets of 2 bits  
Ex: 9 = 1001 = 00,00,…..00,10,01  
First step that algorithm does is to count the number of set bits in each of these 2-bit numbers. As each 2-bit number can have a maximum of 2 set bits. Each of these counts fit into a 2-bit number. That is what the below snippet does.

```c++
i = (i & 0x55555555) + ((i >> 1) & 0x55555555);
```

‘i & F’ preserves only the odd positioned ones. (i>>1) & F preserves only the even positioned ones and gets the even ones to odd positions. Adding them results in each pair of 2-bits having the number of set bits in their corresponding positions.  
Similarly the after next 2 steps we end up having a number which can be seen as 4 8-bit numbers whose sum is the required count.

```
i = (i & 0x33333333) + ((i >> 2) & 0x33333333);
i = (i & 0x0F0F0F0F) + (i >> 4)) & 0x0F0F0F0F);
```

Multiplying this number with 0X01010101 will result in a number whose most significant 8 bits contain the required count. Finally on summing up all these steps we get the following code.

```c++
int NumberOfSetBits32(int i)
{
    i = (i & 0x55555555) + ((i >> 1) & 0x55555555);
    i = (i & 0x33333333) + ((i >> 2) & 0x33333333);
    i = (i & 0x0F0F0F0F) + (i >> 4)) & 0x0F0F0F0F);
    return (i*(0x01010101))>>24;
}
```

Here some more micro optimizations are possible. After giving some thought it can be understood that the 2 lines of code in the below snippet produce the same result.

```c++
i = (i & 0x55555555) + ((i >> 1) & 0x55555555);
i = i - ((i >> 1) & 0x55555555);
```
In general ‘&’ operator is not distributive over ‘+’. But in this case it does. In i and i>>4, each of the eight 4-bit numbers has a maximum value of 4 (fits in 3 bits). And adding these numbers will not cause an overflow in any of the 4-bit slots. So it works in this case. (Think of why it will not work int the previous steps).
```c++
i = (i & 0x0F0F0F0F) + (i >> 4)) & 0x0F0F0F0F);
i = (i & + (i >> 4)) & 0x0F0F0F0F;
```
So finally we arrive at the code for NumberOfSetBits32 as in the 2nd snippet ( NumberOfSetBits64 can be implemented in similar lines).
