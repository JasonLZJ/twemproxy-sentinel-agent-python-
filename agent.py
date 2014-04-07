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

    def restart(self):

    def __del__(self):
        pass

if __name__ == '__main__':
    ag=agent()
    
    config=ag.read_config()
    for key in config.keys():
        print config[key]['sentinel_host']
