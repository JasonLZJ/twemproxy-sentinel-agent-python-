#!/usr/bin/env python

import os,sys
import json
import yaml
import commands
from redis.sentinel import Sentinel
from datetime import *
import time

class agent(object): 
    def __init__(self):
        pass

    #by default,load the agent cnfig file
    def load_config(self,config_file='./conf/agent.yml'):
        self.config_file=config_file
        with open(self.config_file,'r') as fd: 
            self.config = yaml.load(fd)
        return  self.config
    
    #load the twemproxy config file by agent_conf_sn we specified 
    def  load_twem_config(self,agent_conf_sn):
         self.config=self.load_config()
         self.twem_config_file=self.config[agent_conf_sn]['twem_config']
         self.twem_config=self.load_config(self.twem_config_file)
         return self.twem_config
    
    #restart the twemproxy 
    def twem_restart(self,agent_conf_sn):  # conf_sn(config file session name) is 'cli1','cli2' etc. we can regard him as  primary key in sql. 
        self.load_config()
        cmd=self.config[agent_conf_sn]['twem_cmd']
        rs,rt = commands.getstatusoutput(cmd)  # 'rs' means result, 'rt' mean return
        print rs,rt  #debug info
        return  rt  

    def update_twem_master(self,conf_sn,sv_alias,new_ip,new_port):
        self.load_twem_config(conf_sn)    
        self.twem_servers=self.twem_config['twem1']['servers']
        print "[",datetime.now(),"]","[warning] update master:",conf_sn,sv_alias
        for i in range(len(self.twem_servers)):
            if ( self.twem_servers[i].split(" ")[1] == sv_alias ):
                print "[",datetime.now(),"]","old_master :",self.twem_servers[i].split(" ")[0].split(":")
                weight=self.twem_servers[i].split(" ")[0].split(":")[2]
                new_addr=new_ip+':'+str(new_port)+':'+weight+' '+sv_alias
                print "[",datetime.now(),"]","new_master",new_addr 
                self.twem_servers[i]=new_addr
    
        with open(self.twem_config_file,'w') as stream:
            yaml.dump(self.twem_config,stream,allow_unicode=True,default_flow_style=False)

        self.twem_restart(conf_sn)

    #return the twemproxy's master addr (IP:PORT)
    def get_twem_master(self,conf_sn='cli1',sv_alias='mymaster1'):
        self.load_twem_config(conf_sn)
        self.twem_servers=self.twem_config['twem1']['servers']
        for i in range(len(self.twem_servers)):
            if( self.twem_servers[i].split(" ")[1] == sv_alias ):
                self.twem_master=self.twem_servers[i].split(" ")[0].split(':')[0]+':'+self.twem_servers[i].split(" ")[0].split(':')[1]
        #print 'twemproxy_master:',self.twem_master
        return self.twem_master


    #retun the sentinel_master addr 
    def get_sentinel_master(self,conf_sn,sv_alias):
        stats=1
        self.load_config()
        self.sentinel_host=self.config[conf_sn]['sentinel_host']
        self.sentinel_port=self.config[conf_sn]['sentinel_port']
        try:
            self.sentinel=Sentinel([(self.sentinel_host,self.sentinel_port)],socket_timeout=1)
        except :
            print "connect err"

        while stats:
            try:
                self.sentinel_master=self.sentinel.discover_master(sv_alias)
                stats=0
            except:
                time.sleep(0.5)
                print "[",datetime.now(),"]","[erro] get sentinel_master failed..."

        self.sentinel_master=self.sentinel_master[0]+':'+str(self.sentinel_master[1])
        return self.sentinel_master

        #self.sentinel_slave=self.sentinel.discover_slaves(sv_alias)
        #print 'sentinel:',self.sentinel_host,self.sentinel_port
        #print 'sentinel_slaves:',self.sentinel_slave

    def __del__(self):
        pass

if __name__ == '__main__':
    ag=agent()

    config=ag.load_config('./conf/agent.yml')
    sn=config.keys() #get the config file session name  ,just like 'cli1','cli2'......
    print "[",datetime.now(),"]","agent is running..."
    print "[",datetime.now(),"]","session name form agent config file :",sn

    while 1:
        for conf_sn in sn:
            tw_config=ag.load_twem_config(conf_sn)
            sv=[]            # get the 
            for s in tw_config['twem1']['servers']:
                sv.append(s.split(" ")[1])    # get the sv_alias list
            for  sv_alias in sv:
                twem_master=ag.get_twem_master(conf_sn,sv_alias)
                sentinel_master=ag.get_sentinel_master(conf_sn,sv_alias)

                if ( twem_master != sentinel_master ):
                    new_ip=sentinel_master.split(':')[0]
                    new_port=sentinel_master.split(':')[1]
                    ag.update_twem_master(conf_sn,sv_alias,new_ip,new_port)

        time.sleep(1)
