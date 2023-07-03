import pytest
import logging
import paramiko
from clilib import CliInterface
import time
from collections import namedtuple
import pytest_check as check
from config import *
from conftest import *
import re


pytestmark = [pytest.mark.env_name("SNMP_CLI_env"), pytest.mark.cli_dev(Test_Target)]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Qos_manage = namedtuple('Qos_manage', ['Index', 'config', "result_find", "result_error", 'result_not_find', 'grep'])
Qos_manage.__new__.__defaults__ = (None, "", [], [], [], "")

Qos_managegment_DATA = [
Qos_manage(1, "qos enable", 
result_find=["qos enable"],grep="qos"),
Qos_manage(2, "qos enable", 
result_find=["qos enable"],grep="qos"),
Qos_manage(3, "qos disable", 
result_find=["qos disable"],grep="qos"),
Qos_manage(4, "qos disable", 
result_find=["qos disable"],grep="qos"),

]


def Qos_Management(cli_interface_module, data=Qos_manage()): 
    result_find = data.result_find
    result_error = data.result_error
    result_not_find = data.result_not_find
    grep = data.grep

    detail_result = cli_interface_module.exec(data.config) 
    detail_result = '\n'.join(detail_result.split('\n')[1:-1])  

    if len(result_find) != 0:
        for f in result_find:
            result = get_result(cli_interface_module, f"{grep}", False)
            assert (result.find(f)!=-1),f"NOT EXIST {f} in config"
    if len(result_error) != 0:
        for error in result_error:
            assert (detail_result.find(error)!=-1),f"APPLY ERROR DATA"
    if len(result_not_find) != 0:
        for nf in result_not_find:
            result = get_result(cli_interface_module, f"{grep}", False)
            assert (result.find(nf)==-1),f"FIND {data.config} IN CONFIG OF SYSTEM AND NOT TO BE CLEARED"

def test_Qos_Management(cli_interface_module):
    cli_interface_module.change_to_config() 
    for qos in Qos_managegment_DATA:  
        Qos_Management(cli_interface_module, qos)

