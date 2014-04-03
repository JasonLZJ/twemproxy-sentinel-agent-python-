
####agent需要做的事情
1. 侦听sentinel消息,及时获取master的信息
2. 如果master发生变化，则更新nutcracker.yml
3. 重启twemproxy

####agent 配置文件
* redis-sentinel host
* redis-sentinel port
* twemproxy的配置文件路径
* 重启 twemproxy的命令
* agent log路径


####实现思路

1.读取配置文件到config字典（已经实现）
2.与多个sentinel通信（通过pub/sub获取master列表， 如何维护状态？？？）
3.如果发现sentinel主机变更，更新twemproxy配置文件
4.重启twemproxy(单独实现，简单的系统调用)
5.记录日志。。。

