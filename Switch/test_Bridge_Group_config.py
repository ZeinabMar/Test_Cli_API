import pytest
import logging
import paramiko
from clilib import CliInterface
import time
from collections import namedtuple
import pytest_check as check
from config import *
from conftest import *
from Switch.test_Bridge_config import Bridge_definition


pytestmark = [pytest.mark.env_name("SNMP_CLI_env"), pytest.mark.cli_dev(Test_Target)]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Switch = namedtuple('Switch', ['Index', 'config', "result_find", "result_error", 'result_not_find', 'grep'])
Switch.__new__.__defaults__ = (None, "", [], [], [], "")


Switch_DATA = [
 [Switch(1, "no switchport", result_find=["no switchport"], grep="switchport"),
 Switch(1, "bridge-group 1 spanning-tree enable", result_error=["Error code: -1625"], grep="bridge-group")],

 [Switch(2, "switchport", result_find=["switchport"], grep="switchport"),
 Switch(2, "bridge-group 1 spanning-tree enable", result_find=["bridge-group 1 spanning-tree enable"], grep="bridge-group")],

 [Switch(3, "bridge-group 1 spanning-tree disable", result_find=["bridge-group 1 spanning-tree disable"], grep="bridge-group")],
 
 [Switch(4, "no bridge-group 1 spanning-tree disable", result_not_find=["bridge-group 1 spanning-tree"], grep="bridge-group"),
 Switch(4, "no switchport", result_find=["no switchport"], grep="switchport"),],
 ]
 
#[ Switch(3, 1, 1, -1, result="Pass"),

#  Switch(4, 1, 1, 1, result="Pass"),
#  Switch(5, -1, 1, 1, result="Fail"),
#  Switch(6, 1, -1, 1, result="Pass") ]

def Switch_config(cli_interface_module, DATA=[Switch(),Switch()]):   
    for data in DATA:
        result_find = data.result_find
        result_error = data.result_error
        result_not_find = data.result_not_find
        grep = data.grep
        detail_result = cli_interface_module.exec(data.config) 
        detail_result = '\n'.join(detail_result.split('\n')[1:-1])  
        if len(result_find) != 0:
            for f in result_find:
                result = get_result(cli_interface_module, f"{grep}")
                assert (result.find(f)!=-1),f"NOT EXIST {f} in config"
        if len(result_error) != 0:
            for error in result_error:
                assert (detail_result.find(error)!=-1),f"APPLY ERROR DATA"
        if len(result_not_find) != 0:
            for nf in result_not_find:
                result = get_result(cli_interface_module, f"{grep}")
                assert (result.find(nf)==-1),f"FIND {data.config} IN CONFIG OF SYSTEM AND NOT TO BE CLEARED"

@pytest.mark.order(3)        
def test_Switch_config(cli_interface_module):
    cli_interface_module.change_to_config() 
    Bridge_definition(cli_interface_module, bridge_custom[0])
    for port in range(1,2):
        if 1 <= port <=8 :
            cli_interface_module.exec(f"interface ge1/{port}") 
        else:    
            cli_interface_module.exec(f"interface gpon-olt1/{port-8}") 
        for switch in Switch_DATA:
            Switch_config(cli_interface_module, switch)
    cli_interface_module.exec("exit") 
    Bridge_definition(cli_interface_module, bridge_definition_DELETE)
        





