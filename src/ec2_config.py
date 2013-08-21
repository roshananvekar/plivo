# Client configuration file

from plivo_utils import read_config


class EC2Config(object):
    def __init__(self,config_name):
        self.access_key = read_config(config_name,"access_key")
        self.secret_key = read_config(config_name,"secret_key")
        self.region = read_config(config_name,"region")
       
        