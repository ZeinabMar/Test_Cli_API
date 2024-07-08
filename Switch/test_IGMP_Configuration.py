import pytest
import logging
import paramiko
import time
from collections import namedtuple
import pytest_check as check
from config import *
import re
from conftest import *
from Switch.test_Bridge_config import Bridge_definition
from Switch.test_Vlan_config import vlan_management
from Switch.test_Bridge_Group_config import Switch_config
from Switch.test_Uplink_port_Vlan_config import Uplink_Vlan,set_mode_and_check


pytestmark = [pytest.mark.env_name("SNMP_CLI_env"), pytest.mark.cli_dev("shelf_olt")]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

IGMP = namedtuple('IGMP', ['Index', 'config', "result_find", "result_error", 'result_not_find', 'grep'])
IGMP.__new__.__defaults__ = (None, "", [], [], [], "")

IGMP_DATA = [
IGMP(1, "igmp work-mode proxy", result_find=["igmp work-mode proxy", "igmp fast-leave disable", "igmp querier disable"], result_not_find=["igmp mrouter interface"],grep="igmp"),
IGMP(2, "igmp fast-leave enable", result_find=["igmp work-mode proxy", "igmp fast-leave enable", "igmp querier disable"], result_not_find=["igmp mrouter interface"],grep="igmp"),
IGMP(2, "igmp fast-leave disable", result_find=["igmp work-mode proxy", "igmp fast-leave disable", "igmp querier disable"], result_not_find=["igmp mrouter interface"],grep="igmp"),
IGMP(3, "igmp querier enable", result_find=["igmp work-mode proxy", "igmp fast-leave disable", "igmp querier enable"], result_not_find=["igmp mrouter interface"],grep="igmp"),
IGMP(3, "igmp querier disable", result_find=["igmp work-mode proxy", "igmp fast-leave disable", "igmp querier disable"], result_not_find=["igmp mrouter interface"],grep="igmp"),
IGMP(4, "igmp mrouter interface ge1/1", result_find=["igmp mrouter interface ge1/1", "igmp work-mode proxy", "igmp fast-leave disable", "igmp querier disable"],grep="igmp"),
IGMP(5, "igmp mrouter interface ge1/2", result_find=["igmp mrouter interface ge1/2", "igmp work-mode proxy", "igmp fast-leave disable", "igmp querier disable"],grep="igmp"),
IGMP(6, "igmp work-mode snooping", result_find=["igmp work-mode snooping", "igmp mrouter interface ge1/2", "igmp fast-leave disable", "igmp querier disable"],grep="igmp"),
IGMP(2, "no igmp fast-leave disable", result_not_find=["igmp"],grep="igmp"),
IGMP(1, "igmp work-mode proxy", result_find=["igmp work-mode proxy", "igmp fast-leave disable", "igmp querier disable"], result_not_find=["igmp mrouter interface"],grep="igmp"),
IGMP(3, "no igmp work-mode proxy", result_not_find=["igmp"],grep="igmp"),
IGMP(1, "igmp mrouter interface ge1/1", result_find=["igmp mrouter interface ge1/1" ,"igmp work-mode proxy", "igmp fast-leave disable", "igmp querier disable"],grep="igmp"),
IGMP(3, "no igmp querier enable", result_not_find=["igmp"],grep="igmp"),

# IGMP(5, "igmp mrouter interface ge1/1", result_find=["igmp mrouter interface ge1/2"],grep="igmp"), #not to has been applied yet.
]

IGMP_Delete = [
IGMP(1, "no igmp", result_not_find=["igmp work-mode snooping", ],grep="igmp"),
]


def IGMP_Configuration(cli_interface_module, data=IGMP()): 
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

def test_IGMP_Configuration(cli_interface_module):
    cli_interface_module.change_to_config() 
    Bridge_definition(cli_interface_module, bridge_custom[0])
    for vlan in Vlan_Custom:
        vlan_management(cli_interface_module, vlan)
    for port in range(2,3):
        cli_interface_module.exec(f"interface ge1/{port}") 
        Switch_config(cli_interface_module, Switch_Enable)  
        set_mode_and_check(cli_interface_module, "trunk")
        Uplink_Vlan(cli_interface_module, Uplink_Vlan_Trunk)  
    cli_interface_module.exec("exit")  

    cli_interface_module.exec("interface vlanif10")   
    for igmp in IGMP_DATA:
        IGMP_Configuration(cli_interface_module, igmp) 

    cli_interface_module.exec("interface vlanif11")  
    for igmp in IGMP_DATA:
        IGMP_Configuration(cli_interface_module, igmp) 

    # cli_interface_module.exec("interface vlanif10")   
    # for igmp in IGMP_Delete:
    #     IGMP_Configuration(cli_interface_module, igmp) 

    # cli_interface_module.exec("interface vlanif11")  
    # for igmp in IGMP_Delete:
    #     IGMP_Configuration(cli_interface_module, igmp)

    cli_interface_module.exec("exit")    
    for port in range(1,3):
        cli_interface_module.exec(f"interface ge1/{port}") 
        Uplink_Vlan(cli_interface_module, Uplink_Vlan_Trunk_Delete)  
        Switch_config(cli_interface_module, Switch_Disable)
    cli_interface_module.exec("exit")         
    for vlan in Vlan_Custom_DELETE:  
        vlan_management(cli_interface_module, vlan)
    Bridge_definition(cli_interface_module, bridge_definition_DELETE)   

       

