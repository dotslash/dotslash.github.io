---
layout: post
title: What powers yesteapea.com
tags: ['tech' , 'golang', 'python', 'nginx']
comments: true
summary: "How, what and why on yesteapea.com"
---
This article gives a fair amount of detail on how is [yesteapea.com](https://yesteapea.com) up and running (If you are seeing this, it is up and running!). The website has the following components

- Domain/dns setup : Thats how user requests arrive my server(s)
- Flask + gunicorn **python** webserver : contains my slack plugin
- Web server written in **golang** : contains my bookmarks
- **Nginx** : hosts all the **static content** including the blog and acts a proxy for the above 2 servers

### Domain and DNS
I bought the domain from aws. I have one aws virtual machine(aka ec2) with 1 GB ram and 8GB disk. Aws changes the public ip of VM, if the VM dies and DNS change propogations can take upto 2 days. So I have an _'elastic ip'_ which I can bind to any VM in aws. I use this '_elastic ip_' in my DNS entry.

### The python webserver
This server hosts my slack plugin. The plugin shows word/phrase definitions on [urbandictionary](https://urbandictionary.com) and [vocabulary.com](https://vocabulary.com) on user invoking a '_slack slash command_'. For more details [click here](https://yesteapea.com/slack/support-random)

I cache the data from these websites on dynamo db. I also store auth-tokens of slack teams in dynamo db. I use [Flask](http://flask.pocoo.org/) web framework running on [gunicorn](http://gunicorn.org/) server. I played around with markdown blog on flask. This was supposed to be the server serving my website. But later I moved to jekyll for static content and made nginx the entry point for my website


### The Golang webserver
This serves my bookmarks website. I bookmark urls by giving them short names creating a redirect url based on this short name. Ex: [yesteapea.com/red/latency-numbers](http://yesteapea.com/red/latency-numbers) redirects to [gist.github.com/jboner/2841832](https://gist.github.com/jboner/2841832).

I had this working in php before. But later migrated this to [golang](www.golang.org) because I wanted try golang. I store the data on [sqlite](https://www.sqlite.org/), because Im resource constrained (1 ec2 instance; 1 GB ram; see [aws instance-types](https://aws.amazon.com/ec2/instance-types/)). This works pretty well as the data will be pretty small

### Nginx and static data
This blog, homepage and all the static content of the website is generated using [jekyll](https://jekyllrb.com/). The main advantages with jekyll are, I can publish content in markdown and because its static, I can host it very easily (s3, nginx, etc). I put the static hosting in [nginx](https://nginx.org) static hosting.

I use nginx as a proxy server, to host static content and for ssl offloading (I need ssl for the slack app). These are the rules I have on Nginx  

- /slack/* : go to python server
- /under_armour/* : go to python server (this is for my mapmyfitness webapp)
- /bm/* : go to golang webserver
- everything else : lookup in static files  

### Source code

- [Python Server](https://github.com/dotslash/yesteapea.com)
- [Go Server](https://github.com/dotslash/bookmarks)
- [Static Content](https://github.com/dotslash/jekyll-stp)
