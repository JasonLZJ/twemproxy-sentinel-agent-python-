twemproxy-sentinel-agent-python-
================================
agent主要实现监听sentinel消息，当master变更的时候主动更新twempoxy配置，并重启twemproxy。本程序将实现一个agent监听多组sentinel和twemproxy。 

###Redis集群架构简介


![Architecture diagram](https://github.com/breakwang/twemproxy-sentinel-agent-python-/blob/master/misc/twemproxy-agent.png)

[sentinel介绍](http://breakwang.sinaapp.com/?p=198) 

[twemproxy介绍](http://1.breakwang.sinaapp.com/?p=78)
