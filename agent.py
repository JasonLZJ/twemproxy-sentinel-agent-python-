#!/usr/bin/env python
import os,sys
import json
import yaml
import commands
from redis.sentinel import Sentinel

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
    def  load_twem_config(self,agent_conf_sn='cli1'):
         self.twem_config_file=self.config[agent_conf_sn]['twem_config']
         self.twem_config=self.load_config(self.twem_config_file)
         return self.twem_config
        
    #restart the twemproxy 
    def twem_restart(self,agent_conf_sn):  # conf_sn(config file session name) is 'cli1','cli2' etc. we can regard him as  primary key in sql. 
        cmd=self.config[agent_conf_sn]['twem_cmd']
        rs,rt = commands.getstatusoutput(cmd)  # 'rs' means result, 'rt' mean return
        print rs,rt  #debug info
        return  rt  

    def update_twem_master(self,conf_sn='cli1',sv_alias='mymaster1',new_ip='192.168.13.63',new_port=6380):
        self.load_twem_config(conf_sn)           
        self.twem_servers=self.twem_config['twem1']['servers']
        print self.twem_servers
        for i in range(len(self.twem_servers)):
            if ( self.twem_servers[i].split(" ")[1] == sv_alias ):
                print 'old_addr :',self.twem_servers[i].split(" ")[0].split(":")
                weight=self.twem_servers[i].split(" ")[0].split(":")[2]
                new_addr=new_ip+':'+str(new_port)+':'+weight+' '+sv_alias
                print 'new_addr :',new_addr 
                self.twem_servers[i]=new_addr
                print 'changed :',self.twem_servers[i]    
        print self.twem_config
            
        with open(self.twem_config_file,'w') as stream:
            yaml.dump(self.twem_config,stream,allow_unicode=True,default_flow_style=False)
    
    def get_twem_master(self,conf_sn='cli1',sv_alias='mymaster1'):
        print conf_sn,sv_alias,"master addr"

    def get_sentinel_master(self,conf_sn,sv_alias):
        print conf_sn,sv_alias,"master addr"
        
    def __del__(self):
        pass
    

if __name__ == '__main__':
    ag=agent()
    ag.load_config()
    #ag.twem_restart('cli1')
    ag.update_twem_master('cli1','mymaster1','192.168.1.2',6379)
    
