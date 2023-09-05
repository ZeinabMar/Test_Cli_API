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

Port_L3 = namedtuple('Port_L3', ['Index', 'config', "result_find", "result_error", 'result_not_find', 'grep'])
Port_L3.__new__.__defaults__ = (None, "", [], [], [], "")


Port_L3_DATA_1 = [
[Port_L3(1, "ip address 192.168.66.9/24", result_find=["ip address 192.168.66.9/24"], grep="ip address"),
 Port_L3(1, "arp reachable-time 120", result_find=["arp reachable-time 120"], grep="arp"),
 Port_L3(1, "arp timeout 1200", result_find=["arp timeout 1200"], grep="arp")],

[Port_L3(2, "ip address 192.168.66.8/24", result_find=["ip address 192.168.66.8/24"], grep="ip address"),
 Port_L3(2, "arp reachable-time 150", result_find=["arp reachable-time 150"], grep="arp"),
 Port_L3(2, "arp timeout 1500", result_find=["arp timeout 1500"], grep="arp")],

# [Port_L3(3, "no arp timeout 1500", result_find=["arp timeout 1500"], result_error=["Problem"], grep="arp")],
[Port_L3(4, "arp timeout 50", result_find=["arp timeout 1500"], result_error=["Invalid timeout value"], grep="arp"),
 Port_L3(4, "arp reachable-time 8", result_find=["arp reachable-time 150"], result_error=["Error code: -1625"], grep="arp")]
]
Port_L3_DATA_2 = [
[Port_L3(1, "ip address 192.168.66.7/24", result_error=["Error code: -1625"], result_not_find=["ip address 192.168.66.7/24"], grep="ip address"),
 Port_L3(1, "arp reachable-time 120", result_find=["arp reachable-time 120"], grep="arp"),
 Port_L3(1, "arp timeout 1200", result_find=["arp timeout 1200"], grep="arp")]
]

Port_L3_DELETE = [
[Port_L3(1, "no ip address", result_not_find=["no ip address 192.168.66.8/24"], grep="ip address"),
 Port_L3(1, "no arp reachable-time", result_not_find=["arp reachable-time 150"], grep="arp"),
 Port_L3(1, "no arp timeout", result_not_find=["arp timeout 1500"], grep="arp")],
 
[Port_L3(2, "no arp reachable-time", result_not_find=["arp reachable-time 150"], grep="arp"),
 Port_L3(2, "no arp timeout", result_not_find=["arp timeout 1500"], grep="arp")],
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

@pytest.mark.order(7)        
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


                
