#!/usr/bin/env python
import os,sys
import json
import yaml
import commands
from redis.sentinel import Sentinel

class agent(object):
    

    def __init__(self):
        pass
    

    def read_config(self,config_file='./conf/agent.yml'):
        self.config_file=config_file
        with open(self.config_file,'r') as f:
            self.config = yaml.load(f)
        return  self.config

    def restart(self,sn):  # sn(sesion_name) is 'cli1','cli2' etc. we can regard him as  primary key in sql. 
        cmd=self.config[sn]['twem_cmd']
        rs,rt = commands.getstatusoutput(cmd)  # 'rs' means result, 'rt' mean return
        print rs,rt  #debug info
        return  rt  

     def rewrite(self,conf_sn='cli1',sv_alias='mymaster1',new_ip='127.0.0.1',new_port=6379):

        self.config = self.read_config()        # read config
        self.twem_config_file=self.config[conf_sn]['twem_config']
        self.twem_config=self.read_config(self.twem_config_file)
        for i in range(len(self.twem_config['twem1']['servers'])):
            if ( self.twem_config['twem1']['servers'][i].split(" ")[1] == sv_alias ):

                print 'old_addr :',self.twem_config['twem1']['servers'][i].split(" ")[0].split(":")[0],self.twem_config['twem1']['servers'][i].split(" ")[0].split(":")[1]
                print 'new_addr :',new_ip,new_port
                self.twem_config['twem1']['servers'][i].split(" ")[0].split(":")[0]=new_ip
                self.twem_config['twem1']['servers'][i].split(" ")[0].split(":")[1]=new_port
                print 'changed :',self.twem_config['twem1']['servers'][i]
            else:
                print "NOT MATCHING"
    


    def __del__(self):
        pass


if __name__ == '__main__':
    ag=agent()
    ag.rewrite()
    
