corect = 0 
import pytest
import logging
import paramiko
from clilib import CliInterface
import time
from collections import namedtuple
import pytest_check as check
from schema import Use

Test_Target = 'snmp_cli'

pytestmark = [pytest.mark.env_name("SNMP_CLI_env"), pytest.mark.cli_dev(Test_Target)]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Switch = namedtuple('Switch', ['Index', 'switchport','bridgeGroup', 'stpEnable', 'result'])
Switch.__new__.__defaults__ = (None, "no switchport", "no", "disable", ["no switchport","no","disable"])

Switch_DATA = [
#  Switch(1, "no switchport", "", "enable", result=["no switchport","no","disable"]),
 Switch(2, "switchport", "no", "disable", result=["switchport","no","disable"]),

#  Switch(3, 1, 1, -1, result="Pass"),

#  Switch(4, 1, 1, 1, result="Pass"),
#  Switch(5, -1, 1, 1, result="Fail"),
#  Switch(6, 1, -1, 1, result="Pass")     
]


def switch_port(cli_interface_module, switch_port, index=None, result=None):

    cli_interface_module.exec(f"{switch_port}") 
    config_after_set = str(cli_interface_module.exec(f"show running-config interface | grep switchport"))
    config_after_set = '\n'.join(config_after_set.split('\n')[1:-1])
    if result == "switchport":  
        assert (config_after_set.find("switchport")!=-1),f"NOT EXIST ""switchport"" in config "
    else:    
        assert (config_after_set.find("no switchport")!=-1),f"NOT EXIST ""no switchport"" in config"
    

def bridgeGroup(cli_interface_module, bridgeGroup, stpEnable, index=None, result=None):

    cli_interface_module.exec(f"{bridgeGroup} bridge-group 1 spanning-tree {stpEnable}") 
    config_after_set = str(cli_interface_module.exec(f"show running-config interface | grep bridge-group"))
    config_after_set = '\n'.join(config_after_set.split('\n')[1:-1])
    if result[1] == bridgeGroup:
        if bridgeGroup=="":
            assert (config_after_set.find(f"bridge-group 1 spanning-tree {stpEnable}")!=-1),f"NOT EXIST THIS CONFIG Bridge-Group 1 stp {stpEnable}"
        else:  
            assert (config_after_set.find(f"bridge-group 1 spanning-tree {stpEnable}")==-1),f"EXIST THIS CONFIG Bridge-Group 1 stp {stpEnable}"
    else:
        if result[1]=="":
            assert (config_after_set.find(f"bridge-group 1 spanning-tree {stpEnable}")!=-1),f"NO EXIST THIS CONFIG Bridge-Group 1 stp {stpEnable}"
        else:  
            assert (config_after_set.find(f"bridge-group 1 spanning-tree {stpEnable}")==-1),f"EXIST THIS CONFIG Bridge-Group 1 stp {stpEnable}"


def Switch_config(cli_interface_module, data=Switch(), interafce=None, port=None, method=None):
    cli_interface_module.change_to_config()  
    cli_interface_module.exec(f"interface {interafce}{port}") 
    if method == "Set":
        switch_port(cli_interface_module, data.switchport, data.Index, data.result[0])
        bridgeGroup(cli_interface_module, data.bridgeGroup, data.stpEnable, data.Index, data.result[1:])

    elif method == "Delete":   
        bridgeGroup(cli_interface_module, data.bridgeGroup, data.stpEnable, data.Index, data.result[1:])
        switch_port(cli_interface_module, data.switchport, data.Index, data.result[0])


def test_Switch_config(cli_interface_module):
    for ge in range(1,2):
        for switch in Switch_DATA:
            Switch_config(cli_interface_module, switch, "ge1/", ge, "Set")
        Switch_config(cli_interface_module, Switch(), "ge1/", ge, "Delete")