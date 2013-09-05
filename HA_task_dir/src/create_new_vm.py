
from configure_django_vm import ConfigureVM

def create_django_vm():
    config = ConfigureVM()
    vm_id = config.create_custom_vm()
    print "VM ID of new vm:"+str(vm_id)
    

if __name__ == '__main__':
    print "Before creating VM"
    create_django_vm()
    print "After creating VM"
    
