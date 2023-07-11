import pytest
import logging
import paramiko
from clilib import CliInterface
import time
from collections import namedtuple
import pytest_check as check
from config import *
from conftest import *


pytestmark = [pytest.mark.env_name("SNMP_CLI_env"), pytest.mark.cli_dev(Test_Target)]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Static_Rout = namedtuple('Static_Rout', ['Index', 'config', "result_find", "result_error", 'result_not_find', 'grep'])
Static_Rout.__new__.__defaults__ = (None, "", [], [], [], "")


Static_Rout_DATA = [
 Static_Rout(1, "ip route 192.168.45.0 255.255.255.0 192.168.34.65", 
 result_find=["ip route 192.168.45.0 255.255.255.0 192.168.34.65"], grep="ip route"),
  Static_Rout(2, "ip route 192.168.34.0 255.255.255.0 192.168.23.4", 
 result_find=["ip route 192.168.34.0 255.255.255.0 192.168.23.4"], grep="ip route"),
 Static_Rout(3, "ip route 192.168.34.0 255.255.255.0 192.168.23.3", 
 result_find=["ip route 192.168.34.0 255.255.255.0 192.168.23.3"], grep="ip route"),
 ]

Static_Ruote_DATA_DELETE = [
Static_Rout(1, "no ip route 192.168.45.0 255.255.255.0 192.168.34.65", 
 result_not_find=["ip route 192.168.45.0 255.255.255.0 192.168.34.65"], grep="ip route"),
Static_Rout(2, "no ip route 192.168.34.0 255.255.255.0 192.168.23.4", 
 result_not_find=["ip route 192.168.34.0 255.255.255.0 192.168.23.4"], grep="ip route"),
 Static_Rout(3, "no ip route 192.168.34.0 255.255.255.0 192.168.23.3", 
 result_not_find=["ip route 192.168.34.0 255.255.255.0 192.168.23.3"], grep="ip route"),

]

def Static_Rout_configuration(cli_interface_module, data=Static_Rout()):   
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

def test_Static_Rout_configuration(cli_interface_module):
    cli_interface_module.change_to_config() 
    # for staticrout in Static_Rout_DATA:
    #     Static_Rout_configuration(cli_interface_module, staticrout)
    for staticroutdel in Static_Ruote_DATA_DELETE:
        Static_Rout_configuration(cli_interface_module, staticroutdel)
            
