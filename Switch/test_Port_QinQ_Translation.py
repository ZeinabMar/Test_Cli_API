import pytest
import logging
import paramiko
import time
from collections import namedtuple
import pytest_check as check
from config import *
from conftest import *
from Switch.test_Bridge_config import Bridge_definition
from Switch.test_Vlan_config import vlan_management
from Switch.test_Uplink_port_Vlan_config import set_mode_and_check
from Switch.test_Bridge_Group_config import Switch_config


pytestmark = [pytest.mark.env_name("SNMP_CLI_env"), pytest.mark.cli_dev(Test_Target)]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Port_QinQ_Trans = namedtuple('Port_QinQ_Trans', ['Index', 'config', "result_find", "result_error", 'result_not_find', 'grep'])
Port_QinQ_Trans.__new__.__defaults__ = (None, "", [], [], [], "")

uplink_mode = "provider-network" #cusromer-network

Port_QinQ_Translation_Config = [
  Port_QinQ_Trans(1, "switchport qinq trunk mode S-tagged tag 10", result_error=["Error code: -1625"], grep="switchport"),
  Port_QinQ_Trans(2, "switchport qinq trunk mode S-tagged tag 14-17", result_find=["switchport QinQ trunk mode S-tagged tag 14-17 egresstag disable"], grep="switchport"),
  Port_QinQ_Trans(3, "switchport qinq trunk translation svlan-src 14,16 svlan-des 15,17", result_find=["switchport QinQ trunk translation svlan-src 14, 16,  svlan-des 15, 17, "], grep="switchport"),
  Port_QinQ_Trans(4, "switchport qinq trunk translation svlan-src 15 svlan-des 14", result_find=["switchport QinQ trunk translation svlan-src 15, 14, 16,  svlan-des 14, 15, 17, "], grep="switchport"),
  Port_QinQ_Trans(5, "switchport qinq trunk translation svlan-src 18 svlan-des 19", result_error=["Error code: -1625"], grep="switchport"),
  Port_QinQ_Trans(6, "switchport qinq trunk mode S-tagged tag 18-19", result_find=["switchport QinQ trunk mode S-tagged tag 14-19 egresstag disable"], grep="switchport"),
  Port_QinQ_Trans(7, "switchport qinq trunk translation svlan-src 18,14 svlan-des 19,16", result_find=["switchport QinQ trunk translation svlan-src 16, 15, 14, 18,  svlan-des 17, 14, 16, 19, "], grep="switchport"),
  Port_QinQ_Trans(8, "switchport qinq trunk translation svlan-src 14 svlan-des 17", result_find=["switchport QinQ trunk translation svlan-src 16, 15, 14, 18,  svlan-des 17, 14, 16, 19, "], grep="switchport"),

]


Port_QinQ_Translation_Default = [
  Port_QinQ_Trans(1, "no switchport qinq trunk translation svlan-src 15", result_find=["switchport QinQ trunk translation svlan-src 16, 14, 18,  svlan-des 17, 16, 19, "], grep="switchport"),
  Port_QinQ_Trans(2, "no switchport qinq trunk translation svlan-src 16,14,18", result_not_find=["switchport QinQ trunk translation svlan-src"], grep="switchport"),
  Port_QinQ_Trans(3, "no switchport qinq trunk tag 14-19", result_not_find=["switchport QinQ trunk mode S-tagged"], grep="switchport"),
  
]
 
 
 
def Port_QinQ_Translation(cli_interface_module, data=Port_QinQ_Trans(), method="SET"):  
    logger.info(f'PORT QINQ TRANSLATION TEST DATA ------- > {data.Index} IN METHODE {method}')
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

def test_Port_QinQ_Translation(cli_interface_module):
    cli_interface_module.change_to_config() 
    Bridge_definition(cli_interface_module, bridge_service_custom[0])
    for vlan_custom in Vlan_Custom:
        vlan_management(cli_interface_module, vlan_custom)
    for vlan_service in Vlan_Service:  
        vlan_management(cli_interface_module, vlan_service)

    for port in range(1,2):
        if 1 <= port <=8 :
            cli_interface_module.exec(f"interface ge1/{port}") 
        else:    
            cli_interface_module.exec(f"interface gpon-olt1/{port-8}") 

        if uplink_mode == "provider-network":
            Switch_config(cli_interface_module, Switch_Enable)
            set_mode_and_check(cli_interface_module, "provider-network")
        else:
            Switch_config(cli_interface_module, Switch_Enable)
            set_mode_and_check(cli_interface_module, "customer-network")

        for port_qinq in Port_QinQ_Translation_Config:
            Port_QinQ_Translation(cli_interface_module, port_qinq, "SET")

        for port_qinq in Port_QinQ_Translation_Default:
            Port_QinQ_Translation(cli_interface_module, port_qinq, "DELETE")    
        
        Switch_config(cli_interface_module, Switch_Disable)
    cli_interface_module.exec("exit") 
    for vlan_custom_del in Vlan_Custom_DELETE:  
        vlan_management(cli_interface_module, vlan_custom_del)
    for vlan_service_del in Vlan_Service_DELETE:  
        vlan_management(cli_interface_module, vlan_service_del)
    Bridge_definition(cli_interface_module, bridge_definition_DELETE)        
            





