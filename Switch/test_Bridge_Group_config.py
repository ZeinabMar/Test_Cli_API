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

Switch = namedtuple('Switch', ['switchport','bridgeGroup', 'stpEnable', 'result'])
Switch.__new__.__defaults__ = (-1, -1, -1, "Pass")

Switch_DATA = [
 Switch(1, 1, 1, result="Pass"),
#  Switch(1, 1, 1, result="pass"),
#  Switch(1, 1, 1, result="pass")     
]


def switch_port(cli_interface_module, switch_port):
    global corect 
    if switchport == 1:
        cli_interface_module.exec("switchport") 
        result = str(cli_interface_module.exec(f"show running-config | grep switchport"))
        result = '\n'.join(result.split('\n')[1:-1])
        assert (result.find(switchport)!=-1),f"NOT EXIST THIS CONFIG switchport"
        corect = corect+1
    else:    
        cli_interface_module.exec("no switchport") 
        result = str(cli_interface_module.exec(f"show running-config | grep no switchport"))
        result = '\n'.join(result.split('\n')[1:-1])
        assert (result.find(switchport)!=-1),f"NOT EXIST THIS CONFIG no switchport"
        corect = corect+1


def bridgeGroup(cli_interface_module, bridgeGroup, stpEnable):
    global corect
    if bridgeGroup == 1 and stpEnable == -1:
        cli_interface_module.exec("bridge-group 1 spanning-tree disable") 
        result = str(cli_interface_module.exec(f"show running-config | grep bridge-group"))
        result = '\n'.join(result.split('\n')[1:-1])
        assert (result.find("bridge-group 1 spanning-tree disable")!=-1),f"NOT EXIST THIS CONFIG Bridge-Group 1 stp -1"
        corect = corect+1

    elif bridgeGroup == 1 and stpEnable == 1:    
        cli_interface_module.exec("bridge-group 1 spanning-tree enable")  
        result = str(cli_interface_module.exec(f"show running-config | grep bridge-group"))
        result = '\n'.join(result.split('\n')[1:-1])
        assert (result.find("bridge-group 1 spanning-tree enable")!=-1),f"NOT EXIST THIS CONFIG Bridge-Group 1 stp 1"
        corect = corect+1

    elif bridgeGroup==-1:
        cli_interface_module.exec("no bridge-group 1 spanning-tree enable")  
        result = str(cli_interface_module.exec(f"show running-config | grep bridge-group"))
        result = '\n'.join(result.split('\n')[1:-1])
        assert (result.find("bridge-group 1 spanning-tree enable")==-1),f"NOT EXIST THIS CONFIG Bridge-Group -1 "
        corect = corect+1




def Switch_config(cli_interface_module, data=Switch(), interafce=None, port=None):
    cli_interface_module.change_to_config()  
    cli_interface_module.exec(f"interface {interafce}{port}") 
    if result == "Pass":
        switch_port(cli_interface_module, data.switchport)
        bridgeGroup(cli_interface_module, data.bridgeGroup, data.stpEnable)
        assert (correct == 2),f"Pass data have recognized"
        corect = 0
    elif result == "Fail":
        switch_port(cli_interface_module, data.switchport)
        bridgeGroup(cli_interface_module, data.bridgeGroup, data.stpEnable)
        assert (correct <2),f"Fail data have recognized"
        corect = 0

def test_Switch_config(cli_interface_module):
    for ge in range(1,2):
        for switch in Switch_DATA:
            Switch_config(cli_interface_module, switch, "ge1/", ge)
            Switch_config(cli_interface_module, switch, "ge1/", ge)