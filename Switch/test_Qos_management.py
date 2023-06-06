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

Qos_Manage = namedtuple('Qos_Manage', ['QosState', 'result'])
Qos_Manage.__new__.__defaults__ = (None,"Pass")
Qos_Manage_DATA = (
    Qos_Manage("enable","Pass"),
    Qos_Manage("disable", "Pass"),
    Qos_Manage("dis", "Fail"),
    )



def Qos_Management(cli_interface_module, data=Qos_Manage(), method="SET"):

    config_of_qos_set = config_of_qos_check = f"qos {data.QosState}"
    cli_interface_module.change_to_config()   
    if data.result == "Pass":
        if method == "SET":
            cli_interface_module.exec(config_of_qos_set) 
            result = str(cli_interface_module.exec(f"show running-config | grep {config_of_qos_set}"))
            result = '\n'.join(result.split('\n')[1:-1])
            assert (result.find(config_of_qos_set)!=-1),f"NOT EXIST THIS CONFIG {config_of_qos_set}"
                #check.is_in(config_of_bridge[i], result, msg= f"not exist this config {config_of_bridge[i]}")
    elif data.result == "Fail":
        result = cli_interface_module.exec(config_of_qos_set) 
        result = '\n'.join(result.split('\n')[1:-1])
        assert (result.find("Error")!=-1 or result.find("Problem")!=-1),f"NOT EXIST ERROR or PROBLEMS {config_of_qos_set}"
            

def test_Qos_Management(cli_interface_module):
    for data in Qos_Manage_DATA:
        Qos_Management(cli_interface_module, data, "SET")
