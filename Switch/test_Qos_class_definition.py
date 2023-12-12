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

pytestmark = [pytest.mark.env_name("SNMP_CLI_env"), pytest.mark.cli_dev(Test_Target)]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Qos_Class = namedtuple('Qos_Class', ['Index', 'config', "result_find", "result_error", 'result_not_find', 'grep'])
Qos_Class.__new__.__defaults__ = (None, "", [], [], [], "")


Qos_Class_DATA = [
 Qos_Class(1, "class-map B match vlan 10-11", result_find=["class-map B match vlan 10-11"], grep="class-map"),
 Qos_Class(2, "class-map B match vlan 10-11", result_error=["Error code: -1631"]),
 Qos_Class(3, "class-map C match vlan 10", result_find=["class-map C match vlan 10"], grep="class-map"),
 Qos_Class(4, "class-map C match vlan 11", result_find=["class-map C match vlan 10 11"], grep="class-map"),
 Qos_Class(5, "no class-map C match vlan single-vlan", result_find=["class-map C match vlan"], result_not_find=["class-map C match vlan 10 11"], grep="class-map"),
 Qos_Class(6, "no class-map B match vlan vlan-range", result_find=["class-map B match vlan"], result_not_find=["class-map B match vlan 10-11"], grep="class-map"),
 Qos_Class(7, "no class-map C", result_not_find=["class-map C match"], grep="class-map"),
 Qos_Class(8, "no class-map B", result_not_find=["class-map B match"], grep="class-map"),
]

def Qos_class_definition(cli_interface_module, data=Qos_Class()):   
    result_find = data.result_find
    result_error = data.result_error
    result_not_find = data.result_not_find
    grep = data.grep
    detail_result = cli_interface_module.exec(data.config) 
    detail_result = '\n'.join(detail_result.split('\n')[1:-1])  
    if len(result_find) != 0:
        for f in result_find:
            result = get_result(cli_interface_module, f"{grep}", False)
            assert (result.find(f)!=-1),f"NOT EXIST {f} in config"
    if len(result_error) != 0:
        for error in result_error:
            assert (detail_result.find(error)!=-1),f"APPLY ERROR DATA"
    if len(result_not_find) != 0:
        for nf in result_not_find:
            result = get_result(cli_interface_module, f"{grep}", False)
            assert (result.find(nf)==-1),f"FIND {data.config} IN CONFIG OF SYSTEM AND NOT TO BE CLEARED"


def test_Qos_class_definition(cli_interface_module):

    cli_interface_module.change_to_config() 
    Bridge_definition(cli_interface_module, bridge_custom[0])
    for vlan_custom in Vlan_Custom:
        vlan_management(cli_interface_module, vlan_custom)
    Qos_Management(cli_interface_module, Qos_Enable)    


    for qos_class in Qos_Class_DATA:
        Qos_class_definition(cli_interface_module, qos_class)

    Qos_Management(cli_interface_module, Qos_Disable)    
    for vlan_custom in Vlan_Custom_DELETE:
        vlan_management(cli_interface_module, vlan_custom)
    Bridge_definition(cli_interface_module, bridge_definition_DELETE)    
    
