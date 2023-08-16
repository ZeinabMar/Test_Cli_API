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
from Switch.test_Bridge_Mstp_Instance import Bridge_Mstp_Instance_Config
from Switch.test_Bridge_Group_config import Switch_config
from config import *
import re

pytestmark = [pytest.mark.env_name("SNMP_CLI_env"), pytest.mark.cli_dev(Test_Target)]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Port_Mstp = namedtuple('Port_Mstp', ['Index', 'config', "result_find", "result_error", 'result_not_find', 'grep'])
Port_Mstp.__new__.__defaults__ = (None, "", [], [], [], "")


Port_Mstp_Data = [
Port_Mstp(1, "spanning-tree mstp instance 4", result_find=["spanning-tree mstp instance 4"], grep="spanning-tree mstp"),
Port_Mstp(2, "spanning-tree mstp instance 4 path-cost 1000", result_find=["spanning-tree mstp instance 4", "spanning-tree mstp instance 4 path-cost 1000"], grep="spanning-tree mstp"),
Port_Mstp(3, "spanning-tree mstp instance 4 port-priority 48", 
result_find=["spanning-tree mstp instance 4", "spanning-tree mstp instance 4 path-cost 1000", "spanning-tree mstp instance 4 port-priority 48"],
grep="spanning-tree mstp"),
# Port_Mstp(4, "spanning-tree mstp instance 4 port-priority 33", 
# result_find=["spanning-tree mstp instance 4", "spanning-tree mstp instance 4 path-cost 1000", "spanning-tree mstp instance 4 port-priority 48"],
# result_error=["Problem parsing"], grep="spanning-tree mstp"),
Port_Mstp(5, "spanning-tree mstp instance 2", result_find=["spanning-tree mstp instance 2"], grep="spanning-tree mstp"),
Port_Mstp(6, "spanning-tree mstp instance 2 path-cost 1000", result_find=["spanning-tree mstp instance 2", "spanning-tree mstp instance 2 path-cost 1000"], grep="spanning-tree mstp"),
Port_Mstp(7, "spanning-tree mstp instance 2 port-priority 48", 
result_find=["spanning-tree mstp instance 2", "spanning-tree mstp instance 2 path-cost 1000", "spanning-tree mstp instance 2 port-priority 48"],
grep="spanning-tree mstp"),
# Port_Mstp(8, "spanning-tree mstp instance 2 port-priority 33", 
# result_find=["spanning-tree mstp instance 2", "spanning-tree mstp instance 2 path-cost 1000", "spanning-tree mstp instance 2 port-priority 48"],
# result_error=["Problem parsing"], grep="spanning-tree mstp"),
Port_Mstp(9, "no spanning-tree mstp instance 2 port-priority", 
result_find=["spanning-tree mstp instance 2", "spanning-tree mstp instance 2 path-cost 1000"],
grep="spanning-tree bmstp"),
Port_Mstp(10, "no spanning-tree mstp instance 2 path-cost", 
result_find=["spanning-tree mstp instance 2"],
grep="spanning-tree mstp"),
]

Port_Mstp_Delete = [
Port_Mstp(1, "no spanning-tree mstp instance 2", result_not_find=["spanning-tree mstp instance 2"], grep="spanning-tree mstp"),
Port_Mstp(2, "no spanning-tree mstp instance 2 path-cost", result_not_find=["spanning-tree mstp instance 2 path-cost"], grep="spanning-tree mstp"),
Port_Mstp(3, "no spanning-tree mstp instance 2 port-priority", result_not_find=["spanning-tree mstp instance 2 port-priority"], grep="spanning-tree mstp"),
Port_Mstp(1, "no spanning-tree mstp instance 4", result_not_find=["spanning-tree mstp instance 4"], grep="spanning-tree mstp"),
Port_Mstp(2, "no spanning-tree mstp instance 4 path-cost", result_not_find=["spanning-tree mstp instance 4 path-cost"], grep="spanning-tree mstp"),
Port_Mstp(3, "no spanning-tree mstp instance 4 port-priority", result_not_find=["spanning-tree mstp instance 4 port-priority"], grep="spanning-tree mstp"),
]

def Port_Mstp_Config(cli_interface_module, data=[], method="SET", interface=False):  
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

def test_Port_Mstp_Config(cli_interface_module):
    cli_interface_module.change_to_config() 
    # Bridge_definition(cli_interface_module, bridge_service_custom[0])
    # for vlan_custom in Vlan_Custom:
    #     vlan_management(cli_interface_module, vlan_custom)
    # for vlan_service in Vlan_Service:  
    #     vlan_management(cli_interface_module, vlan_service)
    # for bridge_mstp_instance in Bridge_Mstp_Instance_Config_Data:
    #     Bridge_Mstp_Instance_Config(cli_interface_module, bridge_mstp_instance, "SET", False)

    # for port in range(1,3):
    #     if 1 <= port <=8 :
    #         cli_interface_module.exec(f"interface ge1/{port}") 
    #     else:    
    #         cli_interface_module.exec(f"interface gpon-olt1/{port-8}") 
    #     Switch_config(cli_interface_module, Switch_Enable)  
    #     for port_mstp in Port_Mstp_Data:
    #         Bridge_Mstp_Instance_Config(cli_interface_module, port_mstp, "SET", True)

    # for port in range(1,2):
    #     if 1 <= port <=8 :
    #         cli_interface_module.exec(f"interface ge1/{port}") 
    #     else:    
    #         cli_interface_module.exec(f"interface gpon-olt1/{port-8}") 
    #     for port_mstp in Port_Mstp_Delete:
    #         Bridge_Mstp_Instance_Config(cli_interface_module, port_mstp, "DELETE", False)
    #     Switch_config(cli_interface_module, Switch_Disable) 

    for bridge_mstp_instance in Bridge_Mstp_Instance_Config_Delete:
        Bridge_Mstp_Instance_Config(cli_interface_module, bridge_mstp_instance, "DELETE", False)
    for vlan_custom_del in Vlan_Custom_DELETE:  
        vlan_management(cli_interface_module, vlan_custom_del)
    for vlan_service_del in Vlan_Service_DELETE:  
        vlan_management(cli_interface_module, vlan_service_del)
    Bridge_definition(cli_interface_module, bridge_definition_DELETE)    
     
 

                
