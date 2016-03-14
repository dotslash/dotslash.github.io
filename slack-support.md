---
layout: page
title: Slack Dictionary Plugin
comments: true
summary: "Slack dictionary plugin - Support"
permalink: /slack/support-random/
---


NOTE: If you dont care about the details, just check the screenshots the press the 'ADD TO SLACK' button </big>

This plugin is a slash command utils which shows definitions of words from english dictionary and urban dictionary (see [urbandictionary.com](http://www.urbandictionary.com))
<div>
<a href="https://slack.com/oauth/authorize?scope=commands&client_id=16781810420.17757441574">
<img alt="Add Plugin to Slack"
height="40" width="139"
src="https://platform.slack-edge.com/img/add_to_slack.png"
srcset="https://platform.slack-edge.com/img/add_to_slack.png 1x, https://platform.slack-edge.com/img/add_to_slack@2x.png 2x"></a>
</div>

###English dictionary
This is powered by [vocabulary.com](http://www.vocabulary.com). All the meanings in vocabulary.com are listed one after another. Check the example usages

###Urban dictionary
As per urban dictionary, urban dictionary is _a place formerly used to find out about slang, and now a place that teens with no life use as a burn book to whine about celebrities, their friends, etc., let out their sexual frustrations, show off their racist/sexist/homophobic/anti-(insert religion here) opinions, troll, and babble about things they know nothing about._

So no wonder the website is not safe for work (nsfw). However I made some efforts to filter out nsfw content out of the meanings. By default the results are very likely safe for work. But it is possible to explicitly request for the first definition on urban dictionary (which could be nsfw)

###Examples


For **Help** type `/define help`.

![Help](https://yesteapea.com/public/images/slack/help.png "Help")

For definition of a word in both english dictionary and urban dictionary type `/define WORD` (safe for work) or `/define *WORD` (could be not safe for work)

![Definition](https://yesteapea.com/public/images/slack/full.png "Definition")

For definition of a word in specifically english dictionary or in urban dictionary type `/define eng WORD`, `/define urb WORD` respectively
![Specific](https://yesteapea.com/public/images/slack/specific.png "Specific")
