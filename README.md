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

```  	
      global:
          agent_log: /home/logs/nutcracker/agent.log
          delay_loop: 2    

     agents:
         cli1:
             sentinel_host: 10.208.20.241
             sentinel_port: 26403
             twem_config: /usr/local/nutcracker/conf/nutcracker16031.yml
             twem_cmd: /etc/init.d/nutcracker16031 restart
        cli2:
             sentinel_host: 10.208.20.242
             sentinel_port: 26403
             twem_config: /usr/local/nutcracker/conf/nutcracker16031.yml
             twem_cmd: /etc/init.d/nutcracker16031 restart
```

note:
由于本程序是支持代理多个twemproxy实例的，上面的配置文件代理了两个twemproxy，每个twemproxy和后端的配置关系请参考文章开头部分示例。

[sentinel介绍](http://breakwang.sinaapp.com/?p=198) 

[twemproxy介绍](http://1.breakwang.sinaapp.com/?p=78)
