#!/usr/bin/env python

#read configure file


import os,sys
import ConfigParser

config={'sentinel_host':[],
        'sentinel_port':[],
        'twem_config':[],
        'twem_cmd':[],
        'agent_log':[]}

class read_config:
    def __init__(self,config_file_path):
        cf = ConfigParser.ConfigParser()  
        cf.read(config_file_path)

        sv = cf.sections()
        for s in sv:
            s_host = cf.get(s,'sentinel_host')
            config['sentinel_host'].append(s_host)
            
            s_port = cf.get(s,'sentinel_port')
            config['sentinel_port'].append(s_port)

            t_config = cf.get(s,'twem_config')
            config['twem_config'].append(t_config)

            t_cmd = cf.get(s,'twem_cmd')
            config['twem_cmd'].append(t_cmd)

            a_log = cf.get(s,'agent_log')
            config['agent_log'].append(a_log)

        print config

if __name__=="__main__":
    read_config("cli.conf")
