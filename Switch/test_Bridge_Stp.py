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

pytestmark = [pytest.mark.env_name("SNMP_CLI_env"), pytest.mark.cli_dev("shelf_olt")]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Bridge_Stp = namedtuple('Bridge_Stp', ['Index', 'config', "result_find", "result_error", 'result_not_find', 'grep'])
Bridge_Stp.__new__.__defaults__ = (None, "", [], [], [], "")


Bridge_Stp_Data = [
Bridge_Stp(1, "spanning-tree bridge 1 portfast bpdu-filter", result_find=["spanning-tree bridge 1 portfast bpdu-filter"], grep="spanning-tree bridge"),
Bridge_Stp(2, "spanning-tree bridge 1 portfast bpdu-guard", result_find=["spanning-tree bridge 1 portfast bpdu-filter", "spanning-tree bridge 1 portfast bpdu-guard"], grep="spanning-tree bridge"),
Bridge_Stp(3, "spanning-tree bridge 1 errdisable interval 100", 
result_find=["spanning-tree bridge 1 portfast bpdu-filter", "spanning-tree bridge 1 portfast bpdu-guard", "spanning-tree bridge 1 errdisable interval 100"],
grep="spanning-tree bridge"),
Bridge_Stp(4, "spanning-tree bridge 1 errdisable state enable", 
result_find=["spanning-tree bridge 1 portfast bpdu-filter", "spanning-tree bridge 1 portfast bpdu-guard", "spanning-tree bridge 1 errdisable interval 100", "spanning-tree bridge 1 errdisable state enable"],
grep="spanning-tree bridge"),
Bridge_Stp(5, "spanning-tree bridge 1 pathcost method short", 
result_find=["spanning-tree bridge 1 portfast bpdu-filter", "spanning-tree bridge 1 portfast bpdu-guard", 
"spanning-tree bridge 1 errdisable interval 100", "spanning-tree bridge 1 errdisable state enable", "spanning-tree bridge 1 pathcost method short"],
grep="spanning-tree bridge"),
Bridge_Stp(6, "spanning-tree bridge 1 pathcost method long", 
result_find=["spanning-tree bridge 1 portfast bpdu-filter", "spanning-tree bridge 1 portfast bpdu-guard", 
"spanning-tree bridge 1 errdisable interval 100", "spanning-tree bridge 1 errdisable state enable", "spanning-tree bridge 1 pathcost method long"],
grep="spanning-tree bridge"),
Bridge_Stp(7, "spanning-tree bridge 1 errdisable interval 6", 
result_find=["spanning-tree bridge 1 portfast bpdu-filter", "spanning-tree bridge 1 portfast bpdu-guard", 
"spanning-tree bridge 1 errdisable interval 100", "spanning-tree bridge 1 errdisable state enable", "spanning-tree bridge 1 pathcost method long"],
result_error=["Problem parsing"],
grep="spanning-tree bridge"),
 ]


Bridge_Stp_Default = [
Bridge_Stp(1, "no spanning-tree bridge 1 portfast bpdu-filter", result_not_find=["spanning-tree bridge 1 portfast bpdu-filter"], grep="spanning-tree bridge"),
Bridge_Stp(2, "no spanning-tree bridge 1 portfast bpdu-guard", result_not_find=["spanning-tree bridge 1 portfast bpdu-guard"], grep="spanning-tree bridge"),
Bridge_Stp(3, "spanning-tree bridge 1 errdisable state disable", result_not_find=["spanning-tree bridge 1 errdisable state disable"], grep="spanning-tree bridge"),
Bridge_Stp(4, "no spanning-tree bridge 1 errdisable interval 100", result_not_find=["spanning-tree bridge 1 errdisable interval"], grep="spanning-tree bridge"),
Bridge_Stp(5, "no spanning-tree bridge 1 pathcost method", result_not_find=["spanning-tree bridge 1 pathcost method"], grep="spanning-tree bridge"),

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
     
 

                
