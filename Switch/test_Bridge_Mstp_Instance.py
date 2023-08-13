import pytest
import logging
import paramiko
from clilib import CliInterface
import time
from conftest import *
from collections import namedtuple
import pytest_check as check
from Switch.test_Bridge_config import Bridge_definition
from Switch.test_vlan_config import vlan_management
from config import *
import re

pytestmark = [pytest.mark.env_name("SNMP_CLI_env"), pytest.mark.cli_dev(Test_Target)]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Bridge_Mstp = namedtuple('Bridge_Mstp', ['Index', 'config', "result_find", "result_error", 'result_not_find', 'grep'])
Bridge_Mstp.__new__.__defaults__ = (None, "", [], [], [], "")


Bridge_Mstp_Instance_Data = [
Bridge_Mstp(1, "spanning-tree bridge 1 mstp instance 4 vlan 10,12", result_find=["spanning-tree bridge 1 mstp instance 4 vlan 10,12,"], grep="spanning-tree bridge"),
# Bridge_Mstp(2, "spanning-tree bridge 1 mstp instance 4 vlan 10,12", result_find=["spanning-tree bridge 1 mstp instance 4 vlan 10,12,"], result_error=["Error code: -1627"], grep="spanning-tree bridge"),
# Bridge_Mstp(3, "spanning-tree bridge 1 mstp instance 2 vlan 10,11", result_error=["Error code: -1627"], result_not_find=["spanning-tree bridge 1 mstp instance 2"], grep="spanning-tree bridge"),
Bridge_Mstp(4, "spanning-tree bridge 1 mstp instance 2 vlan 11" ,result_find=["spanning-tree bridge 1 mstp instance 2 vlan 11,"], grep="spanning-tree bridge"),
Bridge_Mstp(5, "spanning-tree bridge 1 mstp instance 2 vlan 13" ,result_find=["spanning-tree bridge 1 mstp instance 2 vlan 11,13,"], grep="spanning-tree bridge"),
Bridge_Mstp(6, "spanning-tree bridge 1 mstp instance 2 vlan 12" ,result_find=["spanning-tree bridge 1 mstp instance 2 vlan 11,13,"], result_error=["Error code: -1627"], grep="spanning-tree bridge"),
Bridge_Mstp(7, "no spanning-tree bridge 1 mstp instance 2 vlan 13" ,result_find=["spanning-tree bridge 1 mstp instance 2 vlan 11,"], grep="spanning-tree bridge"),

 
 ]


Bridge_Mstp_Instance_Delete = [
Bridge_Mstp(1, "no spanning-tree bridge 1 mstp instance 2", result_not_find=["spanning-tree bridge 1 mstp instance 2"], grep="spanning-tree bridge"),
Bridge_Mstp(2, "no spanning-tree bridge 1 mstp instance 4", result_not_find=["spanning-tree bridge 1 mstp instance 4"], grep="spanning-tree bridge"),

]

def Bridge_Mstp_Instance_Config(cli_interface_module, data=[], method="SET", interface=True):  
    logger.info(f'BRIDEGE MSTP TEST DATA ------- > {data.Index} IN METHODE {method}')  
    result_find = data.result_find
    result_error = data.result_error
    result_not_find = data.result_not_find
    grep = data.grep
    detail_result = cli_interface_module.exec(data.config) 
    detail_result = '\n'.join(detail_result.split('\n')[1:-1])  
    if len(result_find) != 0:
        for f in result_find:
            result = get_result(cli_interface_module, f"{grep}", interface)
            assert (result.find(f)!=-1),f"NOT EXIST {f} in config"
    if len(result_error) != 0:
        for error in result_error:
            assert (detail_result.find(error)!=-1),f"APPLY ERROR DATA"
    if len(result_not_find) != 0:
        for nf in result_not_find:
            result = get_result(cli_interface_module, f"{grep}", interface)
            assert (result.find(nf)==-1),f"FIND {data.config} IN CONFIG OF SYSTEM AND NOT TO BE CLEARED"

def test_Bridge_Mstp_Instance_Config(cli_interface_module):
    cli_interface_module.change_to_config() 
    # Bridge_definition(cli_interface_module, bridge_service_custom[0])
    # for vlan_custom in Vlan_Custom:
    #     vlan_management(cli_interface_module, vlan_custom)
    # for vlan_service in Vlan_Service:  
    #     vlan_management(cli_interface_module, vlan_service)

    for bridge_mstp_instance in Bridge_Mstp_Instance_Data:
        Bridge_Mstp_Instance_Config(cli_interface_module, bridge_mstp_instance, "SET", False)
    for bridge_mstp_instance in Bridge_Mstp_Instance_Delete:
        Bridge_Mstp_Instance_Config(cli_interface_module, bridge_mstp_instance, "DELETE", False)

    # for vlan_custom_del in Vlan_Custom_DELETE:  
    #     vlan_management(cli_interface_module, vlan_custom_del)
    # for vlan_service_del in Vlan_Service_DELETE:  
    #     vlan_management(cli_interface_module, vlan_service_del)
    # Bridge_definition(cli_interface_module, bridge_definition_DELETE)    
     
 

                
