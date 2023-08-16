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

Bridge_Stp = namedtuple('Bridge_Stp', ['Index', 'config', "result_find", "result_error", 'result_not_find', 'grep'])
Bridge_Stp.__new__.__defaults__ = (None, "", [], [], [], "")


Bridge_Stp_Data = [
Bridge_Stp(1, "spanning-tree autoedge", result_find=["spanning-tree autoedge"], grep="spanning-tree"),
Bridge_Stp(2, "spanning-tree edgeport", result_find=["spanning-tree autoedge", "spanning-tree edgeport"], grep="spanning-tree"),
Bridge_Stp(3, "spanning-tree bpdu-filter default", result_find=["spanning-tree autoedge", "spanning-tree edgeport", "spanning-tree bpdu-filter default"], grep="spanning-tree"),
Bridge_Stp(4, "spanning-tree bpdu-guard default", result_find=["spanning-tree autoedge", "spanning-tree edgeport", "spanning-tree bpdu-filter default", "spanning-tree bpdu-guard default"],
grep="spanning-tree"),
Bridge_Stp(5, "spanning-tree guard root", 
result_find=["spanning-tree autoedge", "spanning-tree edgeport", "spanning-tree bpdu-filter default", "spanning-tree bpdu-guard default", "spanning-tree guard root"],
grep="spanning-tree"),
Bridge_Stp(6, "spanning-tree portfast", 
result_find=["spanning-tree autoedge", "spanning-tree edgeport", "spanning-tree bpdu-filter default", "spanning-tree bpdu-guard default", "spanning-tree guard root", "spanning-tree portfast"],
grep="spanning-tree"),
]


Bridge_Stp_Default = [
Bridge_Stp(1, "no panning-tree autoedge", result_not_find=["spanning-tree autoedge"], grep="spanning-tree bridge"),
Bridge_Stp(2, "no spanning-tree edgeport", result_not_find=["spanning-tree edgeport"], grep="spanning-tree bridge"),
Bridge_Stp(3, "no spanning-tree bpdu-filter default", result_not_find=["spanning-tree bpdu-filter default"], grep="spanning-tree bridge"),
Bridge_Stp(4, "no spanning-tree bpdu-guard default", result_not_find=["spanning-tree bpdu-guard default"], grep="spanning-tree bridge"),
Bridge_Stp(5, "no spanning-tree guard root", result_not_find=["spanning-tree guard root"], grep="spanning-tree bridge"),
Bridge_Stp(6, "no spanning-tree portfast", result_not_find=["spanning-tree portfast"], grep="spanning-tree bridge"),

]

def Bridge_Stp_Configuration(cli_interface_module, data=[], method="SET", interface=True):  
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

def test_Bridge_Stp_Configuration(cli_interface_module):
    cli_interface_module.change_to_config() 
    Bridge_definition(cli_interface_module, bridge_service_custom[0])

    for bridge_stp in Bridge_Stp_Data:
        Bridge_Stp_Configuration(cli_interface_module, bridge_stp, "SET", False)
    for bridge_stp in Bridge_Stp_Default:
        Bridge_Stp_Configuration(cli_interface_module, bridge_stp, "DELETE", False)

    Bridge_definition(cli_interface_module, bridge_definition_DELETE)    
     
 

                
