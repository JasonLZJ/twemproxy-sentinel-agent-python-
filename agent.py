#!/usr/bin/env python
import os,sys
import json
import yaml

class agent(object):
    
    config_file='./conf/agent.conf'

    def __init__(self):
        self.config_file = agent.config_file

    def read_config(self):
        with open(self.config_file,'r') as f:
            self.config = yaml.load(f)
        return  self.config

    def restart(self,sn):  # sn(sesion_name) is 'cli1','cli2' etc. we can regard him as  primary key in sql. 
        cmd=self.config[sn]['twem_cmd']
        rs,rt = commands.getstatusoutput(cmd)  # 'rs' means result, 'rt' mean return
        print rs,rt  #debug info   后期输出到日志
        return  rt  

    def __del__(self):
        pass

if __name__ == '__main__':
    ag=agent()
    
    config=ag.read_config()
    for key in config.keys():
        print config[key]['sentinel_host']
        
    ag.restart('cli3')