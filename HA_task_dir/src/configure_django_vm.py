# To create a VM and configure django server on it


import ec2_config
import plivo_utils
import commands
from time import sleep



aws_section = "AWS"
ha_section = "HA"

class ConfigureVM(object):
    
    def __init__(self):
        self.ec2_cfg = ec2_config.EC2Config(aws_section)
        self.ec2_conn = plivo_utils.get_ec2_connection()
        
        self.current_count = len(self.ec2_conn.get_all_instance_status())
        self.new_count = 0
        self.refresh_flag = False
        
        v_list = self.ec2_conn.get_all_instance_status()
        self.global_vm_list = []
        for vm in v_list:
            self.global_vm_list.append(vm.id)
            
    
    def refresh_vm_count(self):
        num = len(self.ec2_conn.get_all_instance_status())
        if num > self.current_count:
            diff = num - self.current_count 
            self.current_count = self.current_count + diff
            
        
    
    def configure_vm(self,vm_id):
        """
        Configures VM by installing django cms
        """
        print "Command list"
        
    def create_custom_vm(self):
        """
        Creates VM from snapshot template image
        """
        print "Creating a custom VM"
        obj_vm = self.ec2_conn.run_instances(self.ec2_cfg.custom_image_id,
                                             key_name=self.ec2_cfg.key_name,
                                             subnet_id=self.ec2_cfg.subnet_id)
        self.global_vm_list.append(obj_vm.id)
        return obj_vm.instances[0].id
    
    def get_termintaed_vm_count(self):
        now_count = len(self.ec2_conn.get_all_instance_status())
        if now_count < self.current_count:
            print "Terminated instance detected"
            diff = self.current_count - now_count
            self.current_count = self.current_count - diff
            return diff
    
    
    def check_terminated_vms_and_configure(self):
        print "Entering Config"
        
        terminated_count = self.get_termintaed_vm_count()
        if terminated_count > 0:
            for num in xrange(terminated_count):
                vm_id = self.create_custom_vm()
                sleep(5)
                self.current_count +=1
                print "A new VM is brought up"
#                print "Allocating IP address"
#                ip = self.ec2_conn.allocate_address()
#                public_ip = ip.public_ip
#                sleep(45)
#                print "Associating IP address"
#                self.ec2_conn.associate_address(vm_id,public_ip=public_ip)
        self.release_resources()
        self.refresh_vm_count()
        print "Current count of VM's: "+str(self.current_count)
        print "Exiting Config"
        
        sleep(5)
        
    def release_resources(self):
        ip_list = self.ec2_conn.get_all_addresses()
        for ip in ip_list:
            if not ip.association_id:
                self.ec2_conn.release_address(allocation_id=ip.allocation_id)
                print "Releasing public IP"
        
    
    def get_error_instances(self):
        #Right now keeping only as option
        # Returns non responsive VM's
        pass  
    

            
if __name__ == '__main__':
    print "Running HA setup"
    config = ConfigureVM()
    while True:
        config.check_terminated_vms_and_configure()
    print "Finished HA set up"     
            
        
        
        
    
        
                                             
        
        
        
    