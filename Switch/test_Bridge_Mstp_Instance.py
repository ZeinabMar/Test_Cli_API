import pytest
import logging
import paramiko
from clilib import CliInterface
import time
from conftest import *
from collections import namedtuple
import pytest_check as check
from config import *
import re

pytestmark = [pytest.mark.env_name("SNMP_CLI_env"), pytest.mark.cli_dev(Test_Target)]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Bridge_Mstp = namedtuple('Bridge_Mstp', ['Index', 'config', "result_find", "result_error", 'result_not_find', 'grep'])
Bridge_Mstp.__new__.__defaults__ = (None, "", [], [], [], "")


Bridge_Mstp_Instance_Data = [
Bridge_Mstp(1, "spanning-tree bridge 1 mstp instance 4 vlan 10,12", result_find=["spanning-tree bridge 1 mstp instance 4 vlan 10,12,"], grep="spanning-tree bridge"),
Bridge_Mstp(1, "spanning-tree bridge 1 mstp instance 2 vlan 10,11", result_error=["Error code: -1627"], result_not_find=["spanning-tree bridge 1 mstp instance 2"], grep="spanning-tree bridge"),
Bridge_Mstp(1, "spanning-tree bridge 1 mstp instance 2 vlan 11" ,result_find=["spanning-tree bridge 1 mstp instance 2 vlan 11"], grep="spanning-tree bridge"),
Bridge_Mstp(1, "spanning-tree bridge 1 mstp instance 2 vlan 13" ,result_find=["spanning-tree bridge 1 mstp instance 2 vlan 11,13,"], grep="spanning-tree bridge"),
Bridge_Mstp(1, "spanning-tree bridge 1 mstp instance 2 vlan 12" ,result_find=["spanning-tree bridge 1 mstp instance 2 vlan 11,13,"], result_error=["Error code: -1627"], grep="spanning-tree bridge"),
Bridge_Mstp(1, "no spanning-tree bridge 1 mstp instance 2 vlan 13" ,result_find=["spanning-tree bridge 1 mstp instance 2 vlan 11,"], grep="spanning-tree bridge"),

 
 ]


Port_L3_DELETE = [
Bridge_Mstp(1, "no spanning-tree bridge 1 mstp instance 2", result_not_find=["spanning-tree bridge 1 mstp instance 2"], grep="spanning-tree bridge"),
Bridge_Mstp(1, "no spanning-tree bridge 1 mstp instance 4", result_not_find=["spanning-tree bridge 1 mstp instance 4"], grep="spanning-tree bridge"),

]

def Port_L3_configuration(cli_interface_module, DATA=[Port_L3()]): 
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

def test_Port_L3_configuration(cli_interface_module):
    cli_interface_module.change_to_config() 
    for port in range(1,2):
        cli_interface_module.exec(f"interface ge1/{port}") 
        for portl3 in Port_L3_DATA_1:  
            Port_L3_configuration(cli_interface_module, portl3)
        cli_interface_module.exec(f"interface ge1/{port+1}")  
        for portl3 in Port_L3_DATA_2:  
            Port_L3_configuration(cli_interface_module, portl3)
            
        Port_L3_configuration(cli_interface_module, Port_L3_DELETE[1])
        cli_interface_module.exec(f"interface ge1/{port}") 
        Port_L3_configuration(cli_interface_module, Port_L3_DELETE[0])

    # for port in range(9,25):
    #     cli_interface_module.exec(f"interface gpon-olt1/{port-8}") 
    #     for portl3 in Port_L3_DATA_1:  
    #         Port_L3_configuration(cli_interface_module, portl3)
    #     if port != 25:    
    #         cli_interface_module.exec(f"interface gpon-olt1/{port-8+1}")  
    #     else :    
    #         cli_interface_module.exec(f"interface gpon-olt1/{port-8-1}")  
    #     for portl3 in Port_L3_DATA_2:  
    #         Port_L3_configuration(cli_interface_module, portl3)

    #     Port_L3_configuration(cli_interface_module, Port_L3_DELETE[1])
    #     cli_interface_module.exec(f"interface ge1/{port}") 
    #     Port_L3_configuration(cli_interface_module, Port_L3_DELETE[0])


                
