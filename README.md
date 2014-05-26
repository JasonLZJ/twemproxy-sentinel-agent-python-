twemproxy-sentinel-agent-python-
================================
###agent简介：
agent主要实现监听sentinel消息，当master变更的时候主动更新twempoxy配置，并重启twemproxy。本程序实现一个agent监听多组twemproxy(每个twemproxy的后端多组Redis实例需要配置在同一个Sentinel监听)，如下结构所示。 

```
cli1:
    			TwemProxy
		__________|__________
		|					|
	Master1				Master N
Slave1 	SlaveN		Slave 1    Slave N
		|                    |
		__________ ___________
			      |       
		     Redis Sentinel

```
###安装配置：
1. 安装python依赖包 `yaml` 和`redis`
	
		
		wget https://pypi.python.org/packages/source/r/redis/redis-2.9.1.tar.gz
    	tar zxvf redis-2.9.1.tar.gz && cd redis-2.9.1
		python setup.py install
2.配置：
  * 配置文件路径为  `/conf/agent.yml `
  * 举例：
  		
		cli1:
   		 sentinel_host: 127.0.0.1
   		 sentinel_port: 26379
  		  twem_config: /usr/local/nutcracker/conf/nutcracker22121.yml
    	    twem_cmd: /etc/init.d/nutcracker22121 restart
            agent_log: /usr/loca/nutcracker/agent/log/agent1.log
         	cli2:
   		 sentinel_host: 127.0.0.1
            sentinel_port: 26379
            twem_config: /usr/local/nutcracker/conf/nutcracker22122.yml
            twem_cmd: /etc/init.d/nutcracker22122 restart
            agent_log: /usr/loca/nutcracker/agent/log/agent2.log

note:
由于本程序是支持代理多个twemproxy实例的，上面的配置文件代理了两个twemproxy，每个twemproxy和后端的配置关系请参考文章开头部分示例。

[sentinel介绍](http://breakwang.sinaapp.com/?p=198) 

[twemproxy介绍](http://1.breakwang.sinaapp.com/?p=78)
