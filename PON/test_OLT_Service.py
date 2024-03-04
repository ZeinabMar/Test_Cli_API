import pytest
import logging
import paramiko
import time
from conftest import *
from collections import namedtuple
import pytest_check as check
from Switch.test_Bridge_config import Bridge_definition
from Switch.test_Vlan_config import vlan_management
from config import *
import re

pytestmark = [pytest.mark.env_name("SNMP_CLI_env"), pytest.mark.cli_dev(Test_Target)]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

olt_Service = namedtuple('olt_Service', ['Index', 'config', "result_find", "result_error", 'result_not_find', 'grep'])
olt_Service.__new__.__defaults__ = (None, "", [], [], [], "")


olt_Service_Data = [
olt_Service(1, "service-port 1 gemport 1 user-vlan 10 transparent 11", result_find=["service-port 1 gemport 1 user-vlan 10 transparent 11"],
grep="service-port"),

]


olt_Service_Delete = [
olt_Service(1, "no panning-tree autoedge", result_not_find=["spanning-tree autoedge"], grep="spanning-tree bridge"),
]

def OLT_Service_Configuration(cli_interface_module, data=[], method="SET", interface=True):  
    logger.info(f'OLT SERVICE DATA ------- > {data.Index} IN METHODE {method}')  
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

def test_OLT_Service_Configuration(cli_interface_module):
    cli_interface_module.change_to_config() 

    for service_olt in olt_Service_Data:
        OLT_Service_Configuration(cli_interface_module, service_olt, "SET", False)
    for port_stp in olt_Service_Delete:
        OLT_Service_Configuration(cli_interface_module, service_olt, "DELETE", False)

     
 

                
