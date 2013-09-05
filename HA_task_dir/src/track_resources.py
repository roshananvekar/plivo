#!/usr/bin/env python
# Name: Roshan. R. Anvekar

#Background:
# Consider a scenario in which we have 3 tier website deployed over 3 VM's
# Also other cloud artifacts like volumes are created for storage

# Running the following script will pick data elements from config file
# and check the status of cloud resources for sanity.

import ec2_config
import plivo_utils
import os



website_section = "WEBSITE_DETAILS"
aws_section = "AWS"

class WebsiteSanity(object):
    """
    General class with methods to check deployment sanity
    """
    
    def __init__(self):
        # Getting EC2 credentials
        print "Into WebsiteSanity class init"
        self.ec2_cfg = ec2_config.EC2Config(aws_section)
        self.ec2_conn = plivo_utils.get_ec2_connection()
        
        # Getting the key file
        self.private_key_file = os.path.join(os.path.abspath("../"),"data","key_file.pem")
        
        # Getting server IP's
        self.web_srvr_ip = plivo_utils.read_config(website_section, "WEB_SRVR_IP")
        self.app_srvr_ip = plivo_utils.read_config(website_section, "APP_SRVR_IP")
        self.dbase_srvr_ip = plivo_utils.read_config(website_section, "DBASE_SRVR_IP")
        
        #Getting server ID's
        self.web_srvr_id = plivo_utils.read_config(website_section, "WEB_SRVR_ID")
        self.app_srvr_id = plivo_utils.read_config(website_section, "APP_SRVR_ID")
        self.dbase_srvr_id = plivo_utils.read_config(website_section, "DBASE_SRVR_ID")
        print "Out of WebsiteSanity init"
        
    def test_website_sanity(self):
        """
        Common method to check health of all servers under a deployment
        """
        #  Check if servers are reachable
        print "Check if servers are pingable"
#        plivo_utils.vm_ping_check(self.web_srvr_ip)
#        plivo_utils.vm_ping_check(self.app_srvr_ip)
#        plivo_utils.vm_ping_check(self.dbase_srvr_ip)
        
        
        # "Check if servers are reachable 
        print "Check if servers are sshable"
        plivo_utils.vm_ssh_check(self.web_srvr_ip)
        plivo_utils.vm_ssh_check(self.app_srvr_ip)
        plivo_utils.vm_ssh_check(self.dbase_srvr_ip)
        
        # Check the health of the servers
        print "Check the health of the servers"
        web_state = plivo_utils.get_instance_state(self.ec2_conn, self.web_srvr_id)
        web_status = plivo_utils.get_instance_system_status(self.ec2_conn, self.web_srvr_id)
        if str(web_state.strip()) != 'running' and str(web_status.strip()) != "ok":
            raise "Web server is down!!"   
        
        app_state = plivo_utils.get_instance_state(self.ec2_conn, self.app_srvr_id)
        app_status = plivo_utils.get_instance_system_status(self.ec2_conn, self.app_srvr_id)
        if str(app_state.strip()) != 'running' and str(app_status.strip()) != "ok":
            raise "Application server is down!!"  
        
        dbase_state = plivo_utils.get_instance_state(self.ec2_conn, self.dbase_srvr_id)
        dbase_status = plivo_utils.get_instance_system_status(self.ec2_conn, self.dbase_srvr_id)
        if str(dbase_state.strip()) != 'running' and str(dbase_status.strip()) != "ok":
            raise "Database server is down!!"  
        
        # Execute commands in servers
        # This is to check that any command can be executed on VM's to check status
        print "Execute commands in servers"
        command = "echo Hi"
        OUT = plivo_utils.ssh_execute_command(self.web_srvr_ip,
                                              command, 
                                              private_key_file=self.private_key_file)
        
        assert str(OUT),"Hi"
        
        OUT = plivo_utils.ssh_execute_command(self.app_srvr_ip,
                                              command, 
                                              private_key_file=self.private_key_file)
        assert str(OUT),"Hi"
        
        OUT = plivo_utils.ssh_execute_command(self.dbase_srvr_ip,
                                              command, 
                                              private_key_file=self.private_key_file)
        assert str(OUT),"Hi"
        


def check_deployment():
    obj_web_sanity = WebsiteSanity()
    obj_web_sanity.test_website_sanity()
    

if __name__ == '__main__':
    print "Running Deployment check ....."
    check_deployment()
    print "Finished Deployment check ...."
    
                                       
                                       
                        
    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    

