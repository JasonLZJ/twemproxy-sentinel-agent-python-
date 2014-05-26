twemproxy-sentinel-agent-python-
================================
agent主要实现监听sentinel消息，当master变更的时候主动更新twempoxy配置，并重启twemproxy。本程序实现一个agent监听多组twemproxy(每个twemproxy的后端多组Redis实例需要配置在同一个Sentinel监听)，如下图所示。 

```

    			TwemProxy
		__________|__________
		|					|
	Master1				Master N
Slave1 	SlaveN		Slave 1    Slave N
		|                    |
		——————————|——————————
			    	  |       
		  Redis Sentinel

```

[sentinel介绍](http://breakwang.sinaapp.com/?p=198) 

[twemproxy介绍](http://1.breakwang.sinaapp.com/?p=78)
