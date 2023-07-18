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

Port_L2 = namedtuple('Port_L2', ['Index', 'config', "result_find", "result_error", 'result_not_find', 'grep'])
Port_L2.__new__.__defaults__ = (None, "", [], [], [], "")


Port_L2_DATA = [
[Port_L2(1, "no shutdown", result_find=["no shutdown"], grep="shutdown"),
 Port_L2(1, "speed 1G", result_find=["speed 1G"], grep="speed"),
 Port_L2(1, "max-frame 1400", result_find=["max-frame 1400"], grep="max-frame"),
 Port_L2(1, "flowctrl rx", result_find=["flowctrl RX"], grep="flowctrl"),
#  Port_L2(1, "loopback mac", result_find=["loopback mac"], grep="loopback"),
 Port_L2(1, "duplex full", result_find=["duplex full"], grep="duplex"),
 Port_L2(1, "description t", result_find=["description t"], grep="description")],

[Port_L2(2, "no shutdown", result_find=["no shutdown"], grep="shutdown"),
 Port_L2(2, "speed 100G", result_find=["speed 1G"], result_error=["Problem"], grep="speed"),
 Port_L2(2, "max-frame 15000", result_find=["max-frame 1400"], result_error=["Error code: -1625"], grep="max-frame"),
 Port_L2(2, "flowctrl tx", result_find=["flowctrl TX"], grep="flowctrl"),
#  Port_L2(2, "loopback phy", result_find=["loopback mac"],result_error=["Problem"], grep="loopback"),
 Port_L2(2, "duplex half", result_find=["duplex full"],result_error=["Error code: -1625"], grep="duplex"),
 Port_L2(2, "description ", result_find=["description t"], result_error=["Incomplete command"], grep="description")],

 [Port_L2(3, "no shutdown", result_find=["no shutdown"], grep="shutdown"),
 Port_L2(3, "speed 1G", result_find=["speed 1G"], grep="speed"),
 Port_L2(3, "max-frame 1400", result_find=["max-frame 1400"], grep="max-frame"),
 Port_L2(3, "flowctrl both", result_find=["flowctrl Both"], grep="flowctrl"),
#  Port_L2(3, "loopback mac", result_find=["loopback mac"], grep="loopback"),
 Port_L2(3, "duplex full", result_find=["duplex full"], grep="duplex"),
 Port_L2(3, "description t", result_find=["description t"], grep="description")],
]

Port_L2_DEFUALT = [
[Port_L2(1, "no shutdown", result_find=["no shutdown"], grep="shutdown"),
 Port_L2(1, "speed 10G", result_find=["speed 10G"], grep="speed"),
 Port_L2(1, "max-frame 1500", result_find=["max-frame 1500"], grep="max-frame"),
 Port_L2(1, "no flowctrl", result_find=["no flowctrl"], grep="flowctrl"),
#  Port_L2(1, "loopback mac", result_find=["loopback mac"], grep="loopback"),
 Port_L2(1, "duplex full", result_find=["duplex full"], grep="duplex"),
 Port_L2(1, "no description", result_find=["description"], grep="description")],
]

def Uplink_Port_L2_configuration(cli_interface_module, DATA=[Port_L2()]): 
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

def test_Uplink_Port_L2_configuration(cli_interface_module):
    cli_interface_module.change_to_config() 
    for portl2 in Port_L2_DATA: 
        for port in range(1,2):
            cli_interface_module.exec(f"interface ge1/{port}") 
            Uplink_Port_L2_configuration(cli_interface_module, portl2)
            cli_interface_module.exec(f"exit") 
        
    for port in range(1,2):
        cli_interface_module.exec(f"interface ge1/{port}") 
        Uplink_Port_L2_configuration(cli_interface_module, Port_L2_DEFUALT[0])
        cli_interface_module.exec(f"exit") 

                
