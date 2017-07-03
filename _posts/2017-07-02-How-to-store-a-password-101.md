---
layout: post
title: How to store a password 101
comments: true
summary: "How to store a password"
tags: ['tech']
---

Disclaimer : I dont claim expertise in what Im writing about. Feel free to correct me if anything seems off.

In this post I will try to briefly explain how passwords should be _'safely'_ stored in a database. The details of what hashing algorithms to use is beyond the scope of this article (and beyond my knowledge). 

## Definitions
- `hash` : In this context hash is a [cryptographic hash function](https://en.wikipedia.org/wiki/Cryptographic_hash_function). Think of this as a function with these properties
  - The inverse cannot be computed - i.e It is practically impossible to find x if hash(x) is known.
  - The probability of 2 inputs having the same output is 0 for all practical purposes.
- `database` : A database containing everything needed to authenticate a user. 
- `attacker` : A malicous entity who wants to get access to user's real passwords. An attacker could be a rogue developer or an external person.
- `secure` : A method of storing passwords is considered secure if the attacker cannot know user's real passwords even after having access to the database.


## Storing user passwods as is
This is a no brainer. Do not store the passwods as is. If an attacker gets access to the database, they have the password of every single user using the service.

## One way hash
A simple workaround for this problem is to use a one way hash. So if my password is `'really'`, then the user database stores `hash('really')` as my hashed password. When a user enters the password, the `hash(password)` is matched against the one in the database. 

So the database contains the following fields

- user_id
- password_hash : `hash(password)`

If an attacker gains access to the database, they have `hash(password)`. But because the inverse to the hash is not known nothing can be done (not really!)

However, many users have naive passwords and the hash values for these passwords are known - E.g [oranges - 91b07b3169d8a7cb6de940142187c8df](https://md5hashing.net/hash/md5/91b07b3169d8a7cb6de940142187c8df). So when an attacker gets access to the database, they will match the hashed passwords against these known hash values and gain access to those accounts which have known passwords. This is called [Rainbow table attack](https://en.wikipedia.org/wiki/Rainbow_table).

## Salted one way hash 
The problem we had before is that, the hash of certain passwords is known, which means it is not entirely true that the inverse of our hash function is not known. 

Salting is a well known technique which beats this. We generate a random string for each user and hash the result. Essentially we are transforming the user's password to something stronger.
Example : If my password is '`really'` and the salt is `'az@sd3a='`, the `hash('reallyaz@sd3a=')` is stored in the database.
So the database contains the following fields

- user_id
- salt
- salted\_password\_hash : `hash(salt, password)`

If an attacker gains access to the database, they have salt and `hash(salt, password)`. But this is not enough to get the password back from this information. Hence the data is secure. 

That said, brute force is always an option. An attacker can theoritically compute hash values of all strings of size <= 30 and thus be able to know passwords of almost all the users. But that is extremely expensive and not many have the access to such compute power. One way to safe gaurd against this is to use a expensive hash function. This makes brute forcing practically impossible.

## Note to users
- Avoid any website which says it can retrieve your old password, if you forget it.
- Try not to have a common password for multiple websites. All it takes is one leak!
- If 2-factor authentication is an option, go for it.