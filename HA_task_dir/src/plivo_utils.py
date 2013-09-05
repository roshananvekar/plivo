#!/usr/bin/env python
# Name: Roshan. R. Anvekar
# Objective: To create functions and tests to keep track of different resources in cloud
# Cloud Environment: AWS
# 

import ssh
import commands
import os
from time import sleep
import ec2_config
from ConfigParser import SafeConfigParser
import boto.ec2

CONFIG_PATH = os.path.join(os.path.abspath('../'),"config","plivo.conf")


def get_ec2_connection():
    cfg = ec2_config.EC2Config("AWS")
    return boto.ec2.connect_to_region(cfg.region,
                                      aws_access_key_id=cfg.access_key,
                                      aws_secret_access_key=cfg.secret_key)
    
def get_instance_object(ec2_conn,instance_id):
    vm_list = ec2_conn.get_all_instance_status()
    for vm in vm_list:
        if str(vm.id) == str(instance_id):
            return vm
    else:
        return None
    

def get_instance_state(ec2_conn,instance_id):
    obj_vm = get_instance_object(ec2_conn,instance_id)
    return obj_vm.state_name

def get_instance_system_status(ec2_conn,instance_id):
    obj_vm = get_instance_object(ec2_conn,instance_id)
    return obj_vm.system_status.status

def get_volume_object(ec2_conn,volume_id):
    vol_list = ec2_conn.get_all_volumes()
    for vol in vol_list:
        if str(vol.id) == volume_id:
            return vol
    else:
        return None

def get_volume_status(ec2_conn,volume_id):
    obj_vol = get_volume_object(ec2_conn,volume_id)
    return obj_vol.status



def read_config(section,data):
    parser = SafeConfigParser()
    parser.read(CONFIG_PATH)
    return parser.get(section.strip(), data.strip())



def vm_ping_check(vm_ip):
    """This command checks ping to VM """
    cmd = "ping -c 5 "+str(vm_ip)+" > /dev/null"
    status, _ = commands.getstatusoutput(cmd)
    if str(status) != "0":
        raise AssertionError("PING check failed!!")
    
def vm_ssh_check(vm_ip):
    """ This command checks if port 22 of VM is open for SSH connection """
    cmd = "nc -z -v "+str(vm_ip)+" 22"
    status, _ = commands.getstatusoutput(cmd)
    if str(status) != "0":
        raise AssertionError("VM SSH check failed!!")
    
def connect_ssh(ip, private_key_file=None, user='ubuntu'):
    key = ssh.RSAKey.from_private_key_file(private_key_file)
    client = ssh.SSHClient()
    client.set_missing_host_key_policy(ssh.WarningPolicy())
    client.connect(ip, username=user, pkey=key, timeout=5)
    return client

def ssh_execute_command(vm_ip,command,private_key_file=None,user='ubuntu',tries=2,wait=5):
    for x in xrange(tries):
        try:
            conn = connect_ssh(vm_ip, private_key_file=private_key_file, user=user)
            (stdin,stdout,stderr) = conn.exec_command(command)
            output = stdout.read()
            conn.close()
            return output
        except (ssh.AuthenticationException, ssh.SSHException) as e:
            print e
            sleep(wait)
            







