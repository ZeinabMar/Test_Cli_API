import pytest
import logging
import paramiko
from clilib import CliInterface
import time
from collections import namedtuple
import pytest_check as check
from config import *



pytestmark = [pytest.mark.env_name("SNMP_CLI_env"), pytest.mark.cli_dev(Test_Target)]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Uplink_Vlan = namedtuple('Uplink_Vlan', ['Index', 'config', "result_find", "result_error", 'result_not_find'])
Uplink_Vlan.__new__.__defaults__ = (None, "", [], [], [])

Uplink_Vlan_DATA_ACCESS =(    
Uplink_Vlan(1,"switchport access 10", result_find=[f"switchport access 10"]),
Uplink_Vlan(2, "switchport access 10-12", result_find=["switchport access 10"], result_error=["Problem"]),
Uplink_Vlan(3, "switchport access tag 11", result_find=["switchport access 10"], result_error=["Problem"]),
Uplink_Vlan(3, "switchport access -1", result_not_find=["switchport access 10"]),
)


Uplink_Vlan_DATA_TRUNK =(    
Uplink_Vlan(1, "switchport trunk tag 10-11", result_find=[f"switchport trunk tag 10-11"]),
Uplink_Vlan(2, "switchport trunk 12", result_find=["switchport trunk tag 10-11"], result_error=["Invalid argument"]),
Uplink_Vlan(3, "switchport access tag 11", result_find=["switchport trunk tag 10-11"], result_error=["Problem"]),
Uplink_Vlan(4, "no switchport trunk tag 10-11", result_not_find=["switchport trunk tag 10-11"]),
)


Uplink_Vlan_DATA_HYBRID =(    
# Uplink_Vlan(1, "switchport trunk tag 11-12", result_find=[f"switchport trunk tag 11-12"]),
# Uplink_Vlan(2, "switchport access 10", result_find=["switchport access 10"]),
# Uplink_Vlan(3, "switchport trunk tag 10", result_find=["switchport trunk tag 11-12", "switchport access 10"]),
# Uplink_Vlan(4, "switchport access 11", result_find=["switchport trunk tag 12", "switchport access 11"]),
Uplink_Vlan(6, "no switchport access 11", result_not_find=["switchport access 11"]),
Uplink_Vlan(7, "no switchport trunk tag 12", result_not_find=["switchport trunk tag 12"]),
)

def set_mode_and_check(cli_interface_module, mode):
    cli_interface_module.exec(f"switchport mode {mode}") 
    result = get_result(cli_interface_module, "switchport")
    assert (result.find(f"switchport mode {mode}")!=-1),f"NOT EXIST switchport mode {mode} in config "

def Uplink_Vlan(cli_interface_module, data=Uplink_Vlan()):   

    result_find = data.result_find
    result_error = data.result_error
    result_not_find = data.result_not_find


    detail_result = cli_interface_module.exec(data.config) 
    detail_result = '\n'.join(detail_result.split('\n')[1:-1])  

    if len(result_find) != 0:
        for f in result_find:
            result = get_result(cli_interface_module, "switchport")
            assert (result.find(f)!=-1),f"NOT EXIST {f} in config"
    if len(result_error) != 0:
        for error in result_error:
            assert (detail_result.find(error)!=-1),f"APPLY ERROR DATA"
    if len(result_not_find) != 0:
        for nf in result_not_find:
            result = get_result(cli_interface_module, "switchport")
            assert (result.find(nf)==-1),f"FIND {data.config} IN CONFIG OF SYSTEM AND NOT TO BE CLEARED"



def test_Uplink_Vlan(cli_interface_module):

    cli_interface_module.change_to_config() 
    for port in range(1,2):
        for data_mode in [Uplink_Vlan_DATA_HYBRID]:#,Uplink_Vlan_DATA_TRUNK,Uplink_Vlan_DATA_HYBRID
            # if data_mode == Uplink_Vlan_DATA_ACCESS:
            #     if 1 <= port <=8 :
            #         cli_interface_module.exec(f"interface ge1/{port}") 
            #     else:    
            #         cli_interface_module.exec(f"interface gpon-olt1/{port-8}") 
            #     set_mode_and_check(cli_interface_module, "access")
            #     logger.info(f"IN ACCESS MODE")
            #     for data_access in Uplink_Vlan_DATA_ACCESS:
            #         logger.info(f"IN INDEX {data_access.Index} DATA")
            #         Uplink_Vlan(cli_interface_module, data_access)
#*********************************************************************************
            if data_mode == Uplink_Vlan_DATA_TRUNK:
                cli_interface_module.change_to_config()  
                if 1 <= port <=8 :
                    cli_interface_module.exec(f"interface ge1/{port}") 
                else:    
                    cli_interface_module.exec(f"interface gpon-olt1/{port-8}") 
                set_mode_and_check(cli_interface_module, "trunk")
                for data_trunk in Uplink_Vlan_DATA_TRUNK:
                    Uplink_Vlan(cli_interface_module, data_trunk)  
#*********************************************************************************
            if data_mode == Uplink_Vlan_DATA_HYBRID:
                cli_interface_module.change_to_config()  
                if 1 <= port <=8 :
                    cli_interface_module.exec(f"interface ge1/{port}") 
                else:    
                    cli_interface_module.exec(f"interface gpon-olt1/{port-8}")  
                set_mode_and_check(cli_interface_module, "hybrid")
                for data_hybrid in Uplink_Vlan_DATA_HYBRID:
                    Uplink_Vlan(cli_interface_module, data_hybrid)     

              
