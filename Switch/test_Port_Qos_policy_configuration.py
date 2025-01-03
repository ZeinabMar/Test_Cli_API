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
from Switch.test_Qos_management import Qos_Management
from Switch.test_Qos_class_definition import Qos_class_definition
from Switch.test_Qos_policy_configuration_new_featue import Qos_Policy_configuration

pytestmark = [pytest.mark.env_name("SNMP_CLI_env"), pytest.mark.cli_dev("shelf_olt")]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Port_Qos_policy = namedtuple('Port_Qos_policy', ['Index', 'config', "result_find", "result_error", 'result_not_find', 'grep'])
Port_Qos_policy.__new__.__defaults__ = (None, "", [], [], [], "")


Port_Qos_policy_configuration_DATA = [
 Port_Qos_policy(1, "service-policy input policy", result_find=["service-policy input policy"], grep="service-policy"),
 Port_Qos_policy(2, "service-policy input test", result_find=["service-policy input policy"], 
 result_not_find=["service-policy input test"], result_error=["Error code: -1625"], grep="service-policy"),
 Port_Qos_policy(3, "service-policy input policy1", result_find=["service-policy input policy1"], grep="service-policy"), 
 Port_Qos_policy(4, "no service-policy input policy1", result_not_find=["service-policy input policy1"], grep="service-policy"), 
]



def Port_Qos_policy_configuration(cli_interface_module, data=Port_Qos_policy(), port=None, Index=None): 

    result_find = data.result_find
    result_error = data.result_error
    result_not_find = data.result_not_find
    grep = data.grep

    cli_interface_module.exec(f"interface {port}/{Index}") 
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


def test_Port_Qos_policy_configuration(cli_interface_module):

    cli_interface_module.change_to_config() 
    Bridge_definition(cli_interface_module, bridge_custom[0])
    for vlan_custom in Vlan_Custom:
        vlan_management(cli_interface_module, vlan_custom)
    Qos_Management(cli_interface_module, Qos_Enable)    
    for qos_class in Qos_Class_Config:
        Qos_class_definition(cli_interface_module, qos_class)
    for qos_policy in Qos_policy_Config:
        Qos_Policy_configuration(cli_interface_module, qos_policy)

    for port in range(1,2):
        for port_qos_policy in Port_Qos_policy_configuration_DATA:
            Port_Qos_policy_configuration(cli_interface_module, port_qos_policy, "ge1", port)
    # for port in range(9,25):
    #     for port_qos_policy in Port_Qos_policy_configuration_DATA:
    #         Port_Qos_policy_configuration(cli_interface_module, port_qos_policy, "gpon-olt1", port)
    cli_interface_module.exec("exit") 
    for qos_policy in Qos_policy_Config_Delete:
        Qos_Policy_configuration(cli_interface_module, qos_policy)
    for qos_class in Qos_Class_Config_Delete:
        Qos_class_definition(cli_interface_module, qos_class)
    Qos_Management(cli_interface_module, Qos_Disable)    
    for vlan_custom in Vlan_Custom_DELETE:
        vlan_management(cli_interface_module, vlan_custom)
    Bridge_definition(cli_interface_module, bridge_definition_DELETE)     