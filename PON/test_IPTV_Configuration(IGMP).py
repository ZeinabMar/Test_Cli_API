import pytest
import logging
import paramiko
from clilib import CliInterface
import time
from collections import namedtuple
import pytest_check as check
from conftest import *
from config import *
import re
from Switch.test_Bridge_config import Bridge_definition
from Switch.test_Vlan_config import vlan_management
from Switch.test_Bridge_Group_config import Switch_config
from Switch.test_Uplink_port_Vlan_config import Uplink_Vlan,set_mode_and_check
from PON.test_MulticasState import Muticast_Configuration

pytestmark = [pytest.mark.env_name("SNMP_CLI_env"), pytest.mark.cli_dev(Test_Target)]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

IPTV = namedtuple('IPTV', ['Index', 'config', "result_find", "result_error", 'result_not_find', 'grep'])
IPTV.__new__.__defaults__ = (None, "", [], [], [], "")


IPTV_DATA = [
IPTV(1, "remote multicast uni veip vlan 10 priority 7", result_find=["remote multicast uni veip vlan 10 priority 7"],grep="remote"),
IPTV(2, "remote multicast uni veip vlan 11 priority 7", result_error=["Error code: -1559"],grep="remote"),
]

IPTV_DELETE = [IPTV(1, "no remote multicast uni veip vlan 10 priority 7", result_not_find=["remote multicast uni veip vlan 10 priority 7"],grep= "remote")]

def IPTV_Configuration(cli_interface_module, data=IPTV()): 
    result_find = data.result_find
    result_error = data.result_error
    result_not_find = data.result_not_find
    grep = data.grep

    detail_result = cli_interface_module.exec(data.config) 
    detail_result = '\n'.join(detail_result.split('\n')[1:-1])  

    if len(result_find) != 0:
        for f in result_find:
            result = get_result(cli_interface_module, f"{grep}", True)
            assert (result.find(f)!=-1),f"NOT EXIST {f} in config"
    if len(result_error) != 0:
        for error in result_error:
            assert (detail_result.find(error)!=-1),f"APPLY ERROR DATA"
    if len(result_not_find) != 0:
        for nf in result_not_find:
            result = get_result(cli_interface_module, f"{grep}", True)
            assert (result.find(nf)==-1),f"FIND {data.config} IN CONFIG OF SYSTEM AND NOT TO BE CLEARED"



def test_IPTV_Configuration(cli_interface_module):
    cli_interface_module.change_to_config() 
    Bridge_definition(cli_interface_module, bridge_service_custom[0])
    for vlan_custom in Vlan_Custom:
        vlan_management(cli_interface_module, vlan_custom)
    for port in range(2,4):
        cli_interface_module.exec(f"interface gpon-olt1/{port}") 
        Muticast_Configuration(cli_interface_module, Multicast_Enable)
    cli_interface_module.exec("exit") 
    # for port in range(2,4):
        # for onu in range(1,2):
    cli_interface_module.exec(f"interface gpon-onu1/2:3") 
    for iptv in IPTV_DATA:
        IPTV_Configuration(cli_interface_module, iptv)
    cli_interface_module.exec(f"interface gpon-onu1/3:1") 
    for iptv in IPTV_DATA:
        IPTV_Configuration(cli_interface_module, iptv)

    # for port in range(2,4):
    #     for onu in range(1,2):
    cli_interface_module.exec(f"interface gpon-onu1/2:3") 
    for iptv in IPTV_DELETE:
        IPTV_Configuration(cli_interface_module, iptv)
    cli_interface_module.exec(f"interface gpon-onu1/3:1") 
    
    for iptv in IPTV_DELETE:
        IPTV_Configuration(cli_interface_module, iptv)
    for port in range(2,4):
        cli_interface_module.exec(f"interface gpon-olt1/{port}") 
        Muticast_Configuration(cli_interface_module, Multicast_Disable)
    cli_interface_module.exec("exit")     
    for vlan_custom_del in Vlan_Custom_DELETE:  
        vlan_management(cli_interface_module, vlan_custom_del)
    Bridge_definition(cli_interface_module, bridge_definition_DELETE)  
    













    





    
