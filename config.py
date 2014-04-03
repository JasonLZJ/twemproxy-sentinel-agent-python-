#!/usr/bin/env python
import yaml

class read_config(object):

    def __init__(self,config_file = './conf/agent.conf'):
        with open(config_file,'r') as f:
            self.config = yaml.load(f)
            print self.config

    def __del__(self):
        pass

if __name__ == '__main__':
    read_config()
