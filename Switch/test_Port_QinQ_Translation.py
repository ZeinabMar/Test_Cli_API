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
from Switch.test_vlan_config import vlan_management
from Switch.test_Uplink_port_Vlan_config import set_mode_and_check


pytestmark = [pytest.mark.env_name("SNMP_CLI_env"), pytest.mark.cli_dev(Test_Target)]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Port_QinQ_Translation = namedtuple('Port_QinQ_Translation', ['Index', 'config', "result_find", "result_error", 'result_not_find', 'grep'])
Port_QinQ_Translation.__new__.__defaults__ = (None, "", [], [], [], "")


Port_QinQ_Translation = [
  Port_QinQ_Register(1, "switchport qinq registration reg1", result_error=["Error code: -1625"], grep="switchport"),
  Port_QinQ_Register(1, "switchport qinq access 10", result_find=["switchport QinQ access 10"], grep="switchport"),
  Port_QinQ_Register(1, "switchport qinq access 11", result_find=["switchport QinQ access 11"], grep="switchport"),
  Port_QinQ_Register(1, "switchport qinq registration reg1", result_error=["Error code: -1625"], result_not_find=["switchport qinq registration reg1"], grep="switchport"),
  Port_QinQ_Register(1, "switchport qinq access 10", result_find=["switchport QinQ access 10"], grep="switchport"),
  Port_QinQ_Register(1, "switchport qinq registration reg1", result_find=["switchport QinQ registration reg1"], grep="switchport"),
  Port_QinQ_Register(1, "switchport qinq registration reg2", result_find=["switchport QinQ registration reg1"], result_error=["Error code: -1625"], grep="switchport"),
  Port_QinQ_Register(1, "no switchport qinq access 10", result_find= ["switchport QinQ access 10"], result_error=["Error code: -1625"], grep="switchport"),
]


Port_QinQ_Translation_Default = [
  Port_QinQ_Register(1, "no switchport qinq registration reg2", result_not_find=["switchport QinQ registration reg2"], grep="switchport"),
  Port_QinQ_Register(1, "no switchport qinq trunk tag 10,12", result_not_find=["switchport QinQ trunk mode C-tagged tag 10,12 egresstag enable"], grep="switchport"),
]
 
 
 
def Port_QinQ_Translation(cli_interface_module, data=[]):   
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

        for port_qinq in Port_QinQ_Translation:
            Port_QinQ_Translation(cli_interface_module, switch)
        Port_QinQ_Translation(cli_interface_module, Port_QinQ_Translation_Default)
        
        Switch_config(cli_interface_module, Switch_Disable)
   
    # for vlan_custom_del in Vlan_Custom_DELETE:  
    #     vlan_management(cli_interface_module, vlan_custom_del)
    # for vlan_service_del in Vlan_Service_DELETE:  
    #     vlan_management(cli_interface_module, vlan_service_del)
    # Bridge_definition(cli_interface_module, bridge_definition_DELETE)        
            





