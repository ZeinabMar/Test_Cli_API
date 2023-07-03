import pytest
import logging
import paramiko
from clilib import CliInterface
import time
from collections import namedtuple
import pytest_check as check
from config import *
import re


pytestmark = [pytest.mark.env_name("SNMP_CLI_env"), pytest.mark.cli_dev(Test_Target)]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Vlan = namedtuple('Vlan', ['Index', 'config', "result_find", "result_error", 'result_not_find', 'grep'])
Vlan.__new__.__defaults__ = (None, "", [], [], [], "")

Vlan_DATA = [
Vlan(1, "vlan 10 bridge 1 type customer state enable", 
result_find=["vlan 10 bridge 1 type customer state enable"],grep="vlan"),

Vlan(2, "vlan 11 bridge 1 type customer state enable", 
result_find=["vlan 11 bridge 1 type customer state enable"],grep="vlan"),

Vlan(3, "vlan 110 bridge 1 type service-point-point state enable", 
result_find=["vlan 110 bridge 1 type service-point-point state enable"],grep="vlan"),

Vlan(4, "vlan 111 bridge 1 type service-rooted-multipoint state enable", 
result_find=["vlan 111 bridge 1 type service-rooted-multipoint state enable"],grep="vlan"),

Vlan(5, "vlan 111 bridge 1 type customer state enable", 
result_find=["vlan 111 bridge 1 type customer state enable"],grep="vlan"),

Vlan(5, "vlan 111 bridge 1 type customer state disable", 
result_find=["vlan 111 bridge 1 customer state disable"],grep="vlan"),

]

Vlan_DELETE = [
Vlan(1, "no vlan 10 bridge 1 type customer", 
result_not_find=["vlan 10 bridge 1 type customer state enable"],grep= "vlan"),
Vlan(2, "no vlan 11 bridge 1 type customer", 
result_not_find=["vlan 11 bridge 1 type customer state enable"],grep= "vlan"),
Vlan(3, "no vlan 110 bridge 1 type service-point-point", 
result_not_find=["vlan 110 bridge 1 type service-point-point state enable"],grep= "vlan"),
Vlan(4, "no vlan 111 bridge 1 type service-rooted-multipoint", 
result_not_find=["vlan 111 bridge 1 type service-rooted-multipoint state enable"],grep= "vlan"),
Vlan(5, "no vlan 111 bridge 1 type customer", 
result_not_find=["vlan 111 bridge 1 type customer state disable"],grep= "vlan"),

]

def vlan_management(cli_interface_module, data=Vlan()): 
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

def test_vlan_management(cli_interface_module):
    cli_interface_module.change_to_config() 
    # for vlan in Vlan_DATA:
    #     vlan_management(cli_interface_module, vlan)
    for vlan in Vlan_DELETE:  
        vlan_management(cli_interface_module, vlan)
