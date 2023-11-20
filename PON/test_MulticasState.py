import pytest
import logging
import paramiko
from clilib import CliInterface
import time
from collections import namedtuple
import pytest_check as check
from conftest import *
from config import *


pytestmark = [pytest.mark.env_name("SNMP_CLI_env"), pytest.mark.cli_dev(Test_Target)]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Multicas = namedtuple('Multicas', ['Index', 'config', "result_find", "result_error", 'result_not_find', 'grep'])
Multicas.__new__.__defaults__ = (None, "", [], [], [], "")


Multicas_DATA = [
 Multicas(1, "multicast enable", result_find=["multicast enable"],grep="multicast"),
]

Multicas_Disable =  Multicas(1, "multicast disable", result_not_find=["multicast"],grep="multicast")


def Muticast_Configuration(cli_interface_module, data=Multicas()): 
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



def test_Muticast_Configuration(cli_interface_module):
    cli_interface_module.change_to_config() 
    for port in range(2,4):
        cli_interface_module.exec(f"interface gpon-olt1/{port}") 
        for multi in Multicas_DATA:
            Muticast_Configuration(cli_interface_module, multi)
    cli_interface_module.exec("exit") 
    for port in range(2,4):
        cli_interface_module.exec(f"interface gpon-olt1/{port}") 
        Muticast_Configuration(cli_interface_module, Multicas_Disable)
        













    





    
