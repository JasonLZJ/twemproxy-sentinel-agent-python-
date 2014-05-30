#!/usr/bin/env python

import os,sys
import json
import yaml
import commands
from redis.sentinel import Sentinel
from datetime import *
import time
import logging

class agent(object): 
    def __init__(self):
        pass

    #by default,load the agent cnfig file
    def load_config(self,config_file='./conf/agent.yml'):
        self.config_file=config_file
        with open(self.config_file,'r') as fd: 
            self.config = yaml.load(fd)
        return  self.config
    
    def logger(self,path):
    	self.logger=logging.getLogger()
    	self.logger.setLevel(logging.WARNING)
    	fh=logging.FileHandler(path)
    	formatter = logging.Formatter("%(asctime)-15s %(filename)s [%(levelname)-8s] %(message)s")
    	fh.setFormatter(formatter)
    	self.logger.addHandler(fh)
    	return self.logger

    #load the twemproxy config file by agent_conf_sn we specified 
    def  load_twem_config(self,conf_sn):
         self.config=self.load_config()
         self.twem_config_file=self.config['agents'][conf_sn]['twem_config']
         self.twem_config=self.load_config(self.twem_config_file)
         return self.twem_config
     
    #restart the twemproxy 
    def twem_restart(self,conf_sn):  # conf_sn(config file session name) is 'cli1','cli2' etc. we can regard him as  primary key in sql. 
        self.load_config()
        cmd=self.config['agents'][conf_sn]['twem_cmd']
        rs,rt = commands.getstatusoutput(cmd)  # 'rs' means result, 'rt' mean return
        self.logger.warning("%s"%rt)
        return  rt  

    def update_twem_master(self,conf_sn,sv_alias,new_ip,new_port):
        self.load_twem_config(conf_sn)    
        self.twem_servers=self.twem_config['twem1']['servers']
        self.logger.warning("NO,%s:%s twem_master != sentinel_master,Begin update twemproxy "%(conf_sn,sv_alias))

        for i in range(len(self.twem_servers)):
            if ( self.twem_servers[i].split(" ")[1] == sv_alias ):
                self.logger.warning("twem old master:%s"%self.twem_servers[i].split(" ")[0].split(":"))
                #print "[",datetime.now(),"]","old_master :",self.twem_servers[i].split(" ")[0].split(":")
                weight=self.twem_servers[i].split(" ")[0].split(":")[2]
                new_addr=new_ip+':'+str(new_port)+':'+weight+' '+sv_alias
                self.logger.warning("twem new master:%s"%new_addr)
	        #print "[",datetime.now(),"]","new_master",new_addr 
                self.twem_servers[i]=new_addr
    
        with open(self.twem_config_file,'w') as stream:
            yaml.dump(self.twem_config,stream,allow_unicode=True,default_flow_style=False)

        self.twem_restart(conf_sn)

    #return the twemproxy's master addr (IP:PORT)
    def get_twem_master(self,conf_sn,sv_alias):
        self.load_twem_config(conf_sn)
        self.twem_servers=self.twem_config['twem1']['servers']
        for i in range(len(self.twem_servers)):
            if( self.twem_servers[i].split(" ")[1] == sv_alias ):
                self.twem_master=self.twem_servers[i].split(" ")[0].split(':')[0]+':'+self.twem_servers[i].split(" ")[0].split(':')[1]
        #print 'twemproxy_master:',self.twem_master
        self.logger.info("get twemproxy %s:%s master:%s"%(conf_sn,sv_alias,self.twem_master))
        return self.twem_master


    #retun the sentinel_master addr 
    def get_sentinel_master(self,conf_sn,sv_alias):
        stats=1
        self.load_config()
        self.sentinel_host=self.config['agents'][conf_sn]['sentinel_host']
        self.sentinel_port=self.config['agents'][conf_sn]['sentinel_port']
        try:
            self.sentinel=Sentinel([(self.sentinel_host,self.sentinel_port)],socket_timeout=1)
        except :
            self.logger.error('connection to Sentinel %s:%s failed '%(self.sentinel_host,self.sentinel_port))

        while stats:
            try:
                self.sentinel_master=self.sentinel.discover_master(sv_alias)
                stats=0
            except:
                time.sleep(0.5)
                self.logger.error('get %s sentinel %s:%s failed %d times'%(conf_sn,self.sentinel_host,self.sentinel_port,stats))
                stats = stats + 1
		while (stats == 5):
                    stats=0
		    self.logger.error('retry failed,skip this sentinel %s:%s,please check it'%(self.sentinel_host,self.sentinel_port))
        
        self.sentinel_master=self.sentinel_master[0]+':'+str(self.sentinel_master[1])
        if (len(self.sentinel_master)<7):
            return False
            self.logger.error("get sentinel %s,%s master Failed"%(conf_sn,sv_alias))
        else:
            self.logger.info("get sentinel %s,%s master:%s"%(conf_sn,sv_alias,self.sentinel_master))
            return self.sentinel_master
  
    def __del__(self):
        pass

if __name__ == '__main__':
    ag=agent()
    
    #get config,logger,session name 
    config=ag.load_config('./conf/agent.yml')
    logpath=config['global']['agent_log']
    delay_loop=config['global']['delay_loop']
    
    ag.logger(logpath)
    ag.logger.info('agent start working....')
    ag.logger.info('load the agent config: %s'%config)
    sn=config['agents'].keys()
    print " please note:\n agent is running,all infomation will output to file:%s"%logpath 


    while True:
        for conf_sn in sn:
            tw_config=ag.load_twem_config(conf_sn)
            sv=[]            # get the 
            for s in tw_config['twem1']['servers']:
                sv.append(s.split(" ")[1])    # get the sv_alias list
            for  sv_alias in sv:
                twem_master=ag.get_twem_master(conf_sn,sv_alias)
                sentinel_master=ag.get_sentinel_master(conf_sn,sv_alias)

                if ( twem_master != sentinel_master and sentinel_master != False):
                    new_ip=sentinel_master.split(':')[0]
                    new_port=sentinel_master.split(':')[1]
                    ag.update_twem_master(conf_sn,sv_alias,new_ip,new_port)
		elif (sentinel_master != False ):
		    ag.logger.info("OK  %s:%s twem_master==sentinel_master."%(conf_sn,sv_alias))
        time.sleep(delay_loop)
