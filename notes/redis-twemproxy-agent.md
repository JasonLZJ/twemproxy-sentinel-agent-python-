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

1. 读取配置文件到config字典（已经实现）
2. 与多个sentinel通信（通过pub/sub获取master列表， 如何维护状态？？？）
3. 如果发现sentinel主机变更，更新twemproxy配置文件
4. 重启twemproxy(单独实现，简单的系统调用)
5. 记录日志。。。


####参考资料
关于 agent 与 sentinel通信部分可以利用如下API

redis-sentinel发布与订阅
###发布与订阅信息

客户端可以将 Sentinel 看作是一个只提供了订阅功能的 Redis 服务器： 你不可以使用 PUBLISH 命令向这个服务器发送信息， 但你可以用 SUBSCRIBE 命令或者 PSUBSCRIBE 命令， 通过订阅给定的频道来获取相应的事件提醒。

一个频道能够接收和这个频道的名字相同的事件。 比如说， 名为 +sdown 的频道就可以接收所有实例进入主观下线（SDOWN）状态的事件。

通过执行 PSUBSCRIBE * 命令可以接收所有事件信息。

以下列出的是客户端可以通过订阅来获得的频道和信息的格式： 第一个英文单词是频道/事件的名字， 其余的是数据的格式。

注意， 当格式中包含 instance details 字样时， 表示频道所返回的信息中包含了以下用于识别目标实例的内容：

<instance-type> <name> <ip> <port> @ <master-name> <master-ip> <master-port>
@ 字符之后的内容用于指定主服务器， 这些内容是可选的， 它们仅在 @ 字符之前的内容指定的实例不是主服务器时使用。

* +reset-master <instance details> ：主服务器已被重置。
* +slave <instance details> ：一个新的从服务器已经被 Sentinel 识别并关联。
* +failover-state-reconf-slaves <instance details> ：故障转移状态切换到了 reconf-slaves 状态。
* +failover-detected <instance details> ：另一个 Sentinel 开始了一次故障转移操作，或者一个从服务器转换成了主服务器。
* +slave-reconf-sent <instance details> ：领头（leader）的 Sentinel 向实例发送了 SLAVEOF 命令，为实例设置新的主服务器。
* +slave-reconf-inprog <instance details> ：实例正在将自己设置为指定主服务器的从服务器，但相应的同步过程仍未完成。
* +slave-reconf-done <instance details> ：从服务器已经成功完成对新主服务器的同步。
* -dup-sentinel <instance details> ：对给定主服务器进行监视的一个或多个 Sentinel 已经因为重复出现而被移除 —— 当 Sentinel 实例重启的时候，就会出现这种情况。
* +sentinel <instance details> ：一个监视给定主服务器的新 Sentinel 已经被识别并添加。
* +sdown <instance details> ：给定的实例现在处于主观下线状态。
* -sdown <instance details> ：给定的实例已经不再处于主观下线状态。
* +odown <instance details> ：给定的实例现在处于客观下线状态。
* -odown <instance details> ：给定的实例已经不再处于客观下线状态。
* +new-epoch <instance details> ：当前的纪元（epoch）已经被更新。
* +try-failover <instance details> ：一个新的故障迁移操作正在执行中，等待被大多数 
* Sentinel 选中（waiting to be elected by the majority）。
* +elected-leader <instance details> ：赢得指定纪元的选举，可以进行故障迁移操作了。
* +failover-state-select-slave <instance details> ：故障转移操作现在处于 select- slave 状态 —— Sentinel 正在寻找可以升级为主服务器的从服务器。
* no-good-slave <instance details> ：Sentinel 操作未能找到适合进行升级的从服务器。Sentinel 会在一段时间之后再次尝试寻找合适的从服务器来进行升级，又或者直接放弃执行故障转移操作。
* selected-slave <instance details> ：Sentinel 顺利找到适合进行升级的从服务器。
* failover-state-send-slaveof-noone <instance details> ：Sentinel 正在将指定的从服务器升级为主服务器，等待升级功能完成。
* failover-end-for-timeout <instance details> ：故障转移因为超时而中止，不过最终所有从服务器都会开始复制新的主服务器（slaves will eventually be configured to replicate with the new master anyway）。
* failover-end <instance details> ：故障转移操作顺利完成。所有从服务器都开始复制新的主服务器了。
* +switch-master <master name> <oldip> <oldport> <newip> <newport> ：配置变更，主服务器的 IP 和地址已经改变。 这是绝大多数外部用户都关心的信息。
* +tilt ：进入 tilt 模式。
* -tilt ：退出 tilt 模式。
