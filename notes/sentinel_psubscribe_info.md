###只能使用redis.sentinel来监听master切换消息了

		sentinel=Sentinel([('10.209.10.30',46390)],socket_timeout=0.1)
		>>> sentinel.discover_master('mymaster1')
		('10.209.10.30', 6390)
		>>> sentinel.discover_master('mymaster2')
		('10.209.10.31', 6390)



----
###redis.py对pubsub支持的不够好[(参考文章)](https://github.com/andymccurdy/redis-py/issues/151#issuecomment-1545015)
当master宕掉之后。通过pub/sub监听到所有的信息,我们可以通过 psubscribe 中的某些信息来监听是否进行了切换。

>[root@nb-b-kvdb-10-32 ~]# /usr/local/redis/bin/redis-cli -h 10.209.10.31 -p 46390
10.209.10.31:46390> psubscribe *
Reading messages... (press Ctrl-C to quit)
1) "psubscribe"
2) "*"
3) (integer) 1
1) "pmessage"
2) "*"
3) "+sdown"
4) "master mymaster1 10.209.10.30 6390"
1) "pmessage"
2) "*"
3) "+odown"
4) "master mymaster1 10.209.10.30 6390 #quorum 2/2"
1) "pmessage"
2) "*"
3) "+new-epoch"
4) "1"
1) "pmessage"
2) "*"
3) "+try-failover"
4) "master mymaster1 10.209.10.30 6390"
1) "pmessage"
2) "*"
3) "+vote-for-leader"
4) "fa23c37bb64f0a1a30ab046df3b3f70e761a389c 1"
1) "pmessage"
2) "*"
3) "+elected-leader"
4) "master mymaster1 10.209.10.30 6390"
1) "pmessage"
2) "*"
3) "+failover-state-select-slave"
4) "master mymaster1 10.209.10.30 6390"
1) "pmessage"
2) "*"
3) "+selected-slave"
4) "slave 10.209.10.30:6391 10.209.10.30 6391 @ mymaster1 10.209.10.30 6390"
1) "pmessage"
2) "*"
3) "+failover-state-send-slaveof-noone"
4) "slave 10.209.10.30:6391 10.209.10.30 6391 @ mymaster1 10.209.10.30 6390"
1) "pmessage"
2) "*"
3) "+failover-state-wait-promotion"
4) "slave 10.209.10.30:6391 10.209.10.30 6391 @ mymaster1 10.209.10.30 6390"
1) "pmessage"
2) "*"
3) "+promoted-slave"
4) "slave 10.209.10.30:6391 10.209.10.30 6391 @ mymaster1 10.209.10.30 6390"
1) "pmessage"
2) "*"
3) "+failover-state-reconf-slaves"
4) "master mymaster1 10.209.10.30 6390"
1) "pmessage"
2) "*"
3) "+failover-end"
4) "master mymaster1 10.209.10.30 6390"
1) "pmessage"
2) "*"
3) "+switch-master"
4) "mymaster1 10.209.10.30 6390 10.209.10.30 6391"
1) "pmessage"
2) "*"
3) "+slave"
4) "slave 10.209.10.30:6390 10.209.10.30 6390 @ mymaster1 10.209.10.30 6391"
1) "pmessage"
2) "*"
3) "+sdown"
4) "slave 10.209.10.30:6390 10.209.10.30 6390 @ mymaster1 10.209.10.30 6391"
^C
[root@nb-b-kvdb-10-32 ~]# /usr/local/redis/bin/redis-cli -h 10.209.10.31 -p 46390
10.209.10.31:46390> psubscribe +switch-master*
Reading messages... (press Ctrl-C to quit)
1) "psubscribe"
2) "+switch-master*"
3) (integer) 1
1) "pmessage"
2) "+switch-master*"
3) "+switch-master"
4) "mymaster1 10.209.10.30 6391 10.209.10.30 6390"