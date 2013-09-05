# Client configuration file

from plivo_utils import read_config


class EC2Config(object):
    def __init__(self,config_name):
        self.access_key = read_config(config_name,"access_key")
        self.secret_key = read_config(config_name,"secret_key")
        self.region = read_config(config_name,"region")
        self.image_id = read_config(config_name,"image_id")
        self.flavor_id = read_config(config_name,"flavor_id")
        self.key_name = read_config(config_name,"key_name")
        self.security_group = read_config(config_name,"security_group")
        self.subnet_id = read_config(config_name,"subnet_id")
        self.custom_image_id = read_config(config_name,"custom_image_id")


       
        