import pytest
import logging
import paramiko
from clilib import CliInterface
import time
from collections import namedtuple
import pytest_check as check
from schema import Use
from config import *

Test_Target = 'snmp_cli'

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

 [Switch(3, "switchport", result_find=["switchport"], grep="switchport"),
 Switch(3, "bridge-group 1 spanning-tree disable", result_find=["bridge-group 1 spanning-tree disable"], grep="bridge-group")]]
 
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

def test_Switch_config(cli_interface_module):
    cli_interface_module.change_to_config() 
    for port in range(1,2):
        if 1 <= port <=8 :
            cli_interface_module.exec(f"interface ge1/{port}") 
        else:    
            cli_interface_module.exec(f"interface gpon-olt1/{port-8}") 
        for switch in Switch_DATA:
            Switch_config(cli_interface_module, switch)
            














# Switch = namedtuple('Switch', ['Index', 'switchport','bridgeGroup', 'stpEnable', 'result'])
# Switch.__new__.__defaults__ = (None, "no switchport", "no", "disable", ["no switchport","no","disable"])

# Switch_DATA = [
# #  Switch(1, "no switchport", "", "enable", result=["no switchport","no","disable"]),
#  Switch(2, "switchport", "no", "disable", result=["switchport","no","disable"]),

# #  Switch(3, 1, 1, -1, result="Pass"),

# #  Switch(4, 1, 1, 1, result="Pass"),
# #  Switch(5, -1, 1, 1, result="Fail"),
# #  Switch(6, 1, -1, 1, result="Pass")     
# ]


# def switch_port(cli_interface_module, switch_port, index=None, result=None):

#     cli_interface_module.exec(f"{switch_port}") 
#     config_after_set = str(cli_interface_module.exec(f"show running-config interface | grep switchport"))
#     config_after_set = '\n'.join(config_after_set.split('\n')[1:-1])
#     if result == "switchport":  
#         assert (config_after_set.find("switchport")!=-1),f"NOT EXIST ""switchport"" in config "
#     else:    
#         assert (config_after_set.find("no switchport")!=-1),f"NOT EXIST ""no switchport"" in config"
    

# def bridgeGroup(cli_interface_module, bridgeGroup, stpEnable, index=None, result=None):

#     cli_interface_module.exec(f"{bridgeGroup} bridge-group 1 spanning-tree {stpEnable}") 
#     config_after_set = str(cli_interface_module.exec(f"show running-config interface | grep bridge-group"))
#     config_after_set = '\n'.join(config_after_set.split('\n')[1:-1])
#     if result[1] == bridgeGroup:
#         if bridgeGroup=="":
#             assert (config_after_set.find(f"bridge-group 1 spanning-tree {stpEnable}")!=-1),f"NOT EXIST THIS CONFIG Bridge-Group 1 stp {stpEnable}"
#         else:  
#             assert (config_after_set.find(f"bridge-group 1 spanning-tree {stpEnable}")==-1),f"EXIST THIS CONFIG Bridge-Group 1 stp {stpEnable}"
#     else:
#         if result[1]=="":
#             assert (config_after_set.find(f"bridge-group 1 spanning-tree {stpEnable}")!=-1),f"NO EXIST THIS CONFIG Bridge-Group 1 stp {stpEnable}"
#         else:  
#             assert (config_after_set.find(f"bridge-group 1 spanning-tree {stpEnable}")==-1),f"EXIST THIS CONFIG Bridge-Group 1 stp {stpEnable}"


# def Switch_config(cli_interface_module, data=Switch(), interafce=None, port=None, method=None):
#     cli_interface_module.change_to_config()  
#     cli_interface_module.exec(f"interface {interafce}{port}") 
#     if method == "Set":
#         switch_port(cli_interface_module, data.switchport, data.Index, data.result[0])
#         bridgeGroup(cli_interface_module, data.bridgeGroup, data.stpEnable, data.Index, data.result[1:])

#     elif method == "Delete":   
#         bridgeGroup(cli_interface_module, data.bridgeGroup, data.stpEnable, data.Index, data.result[1:])
#         switch_port(cli_interface_module, data.switchport, data.Index, data.result[0])


# def test_Switch_config(cli_interface_module):
#     for ge in range(1,2):
#         for switch in Switch_DATA:
#             Switch_config(cli_interface_module, switch, "ge1/", ge, "Set")
#         Switch_config(cli_interface_module, Switch(), "ge1/", ge, "Delete")