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
Switch.__new__.__defaults__ = (None, -1, -1, -1, "Pass")

Switch_DATA = [
 Switch(1, -1, 1, -1, result="Fail"),
 Switch(2, 1, -1, -1, result="Pass"),
 Switch(3, 1, 1, -1, result="Pass"),
 Switch(4, 1, 1, 1, result="Pass"),
 Switch(5, -1, 1, 1, result="Fail"),
 Switch(6, 1, -1, 1, result="Pass")     
]


def switch_port(cli_interface_module, switch_port, index=None):
    global corect
    if index != 1 and index != 5:
        if switch_port == 1:
            cli_interface_module.exec("switchport") 
            result = str(cli_interface_module.exec(f"show running-config interface | grep switchport"))
            result = '\n'.join(result.split('\n')[1:-1])
            assert (result.find("switchport")!=-1),f"NOT EXIST THIS CONFIG switchport"
            corect = corect+1
        else:    
            cli_interface_module.exec("no switchport") 
            result = str(cli_interface_module.exec(f"show running-config interface | grep no switchport"))
            result = '\n'.join(result.split('\n')[1:-1])
            assert (result.find("no switchport")!=-1),f"NOT EXIST THIS CONFIG no switchport"
            corect = corect+1
    elif index ==1 :
        cli_interface_module.exec("no switchport") 
        result = str(cli_interface_module.exec(f"show running-config interface | grep no switchport"))
        result = '\n'.join(result.split('\n')[1:-1])
        assert (result.find("no switchport")!=-1),f" EXIST THIS CONFIG switchport"
        corect = corect+1
    elif index == 5:    
        cli_interface_module.exec("no switchport") 
        result = str(cli_interface_module.exec(f"show running-config interface | grep no switchport"))
        result = '\n'.join(result.split('\n')[1:-1])
        assert (result.find("no switchport")==-1),f" EXIST THIS CONFIG no switchport"
        corect = corect+1



def bridgeGroup(cli_interface_module, bridgeGroup, stpEnable, index=None):
    global corect
    if (index != 1) and (index != 5):
        if bridgeGroup == 1 and stpEnable == -1:
            cli_interface_module.exec("bridge-group 1 spanning-tree disable") 
            result = str(cli_interface_module.exec(f"show running-config interface | grep bridge-group"))
            result = '\n'.join(result.split('\n')[1:-1])
            assert (result.find("bridge-group 1 spanning-tree disable")!=-1),f"NOT EXIST THIS CONFIG Bridge-Group 1 stp -1"
            corect = corect+1

        elif bridgeGroup == 1 and stpEnable == 1:    
            cli_interface_module.exec("bridge-group 1 spanning-tree enable")  
            result = str(cli_interface_module.exec(f"show running-config interface | grep bridge-group"))
            result = '\n'.join(result.split('\n')[1:-1])
            assert (result.find("bridge-group 1 spanning-tree enable")!=-1),f"NOT EXIST THIS CONFIG Bridge-Group 1 stp 1"
            corect = corect+1

        elif bridgeGroup==-1 and stpEnable == -1:
            cli_interface_module.exec("no bridge-group 1 spanning-tree disable")   
            result = str(cli_interface_module.exec(f"show running-config | grep bridge-group"))
            result = '\n'.join(result.split('\n')[1:-1])
            assert (result.find("bridge-group 1 spanning-tree diasble")==-1),f"NOT EXIST THIS CONFIG Bridge-Group -1 "
            corect = corect+1  

        elif bridgeGroup==-1 and stpEnable == 1:
            cli_interface_module.exec("no bridge-group 1 spanning-tree enable")   
            result = str(cli_interface_module.exec(f"show running-config | grep bridge-group"))
            result = '\n'.join(result.split('\n')[1:-1])
            assert (result.find("bridge-group 1 spanning-tree diasble")==-1),f"NOT EXIST THIS CONFIG Bridge-Group -1 "
            corect = corect+1  

    elif index == 1:
            cli_interface_module.exec("bridge-group 1 spanning-tree disable") 
            result = str(cli_interface_module.exec(f"show running-config interface | grep bridge-group"))
            result = '\n'.join(result.split('\n')[1:-1])
            assert (result.find("bridge-group 1 spanning-tree disable")==-1),f"EXIST THIS CONFIG Bridge-Group 1 stp -1"
            corect = corect+1
    elif index == 5 :  
        # cli_interface_module.exec("bridge-group 1 spanning-tree enable") 
        result = str(cli_interface_module.exec(f"show running-config interface | grep bridge-group"))
        result = '\n'.join(result.split('\n')[1:-1])
        assert (result.find("bridge-group 1 spanning-tree enable")!=-1),f"NO EXIST THIS CONFIG Bridge-Group 1 stp -1"
        corect = corect+1     


def Switch_config(cli_interface_module, data=Switch(), interafce=None, port=None, method=None):
    global corect
    cli_interface_module.change_to_config()  
    cli_interface_module.exec(f"interface {interafce}{port}") 
    if data.result == "Pass":
        if method == "Set":
            switch_port(cli_interface_module, data.switchport, data.Index)
            bridgeGroup(cli_interface_module, data.bridgeGroup, data.stpEnable, data.Index)
        elif method == "Delete":   
            bridgeGroup(cli_interface_module, data.bridgeGroup, data.stpEnable, data.Index)
            switch_port(cli_interface_module, data.switchport, data.Index)
        assert (corect == 2),f"Pass data have recognized"
        corect = 0
    elif data.result == "Fail":
        switch_port(cli_interface_module, data.switchport, data.Index)
        bridgeGroup(cli_interface_module, data.bridgeGroup, data.stpEnable, data.Index)
        assert (corect == 2),f"Fail data have recognized"
        corect = 0

def test_Switch_config(cli_interface_module):
    for ge in range(1,2):
        for switch in Switch_DATA:
            Switch_config(cli_interface_module, switch, "ge1/", ge, "Set")
        Switch_config(cli_interface_module, Switch(-1,-1,-1), "ge1/", ge, "Delete")