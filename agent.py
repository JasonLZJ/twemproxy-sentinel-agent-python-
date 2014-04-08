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

    def rewrite(self,sn='cli1',ip='127.0.0.1',port=26379):
        config = self.read_config()
        twem_config_file=config[sn]['twem_config']
        print twem_config_file
        twem_config=self.read_config(twem_config_file)
        print twem_config
    


    def __del__(self):
        pass


if __name__ == '__main__':
    ag=agent()
    ag.rewrite()
    
