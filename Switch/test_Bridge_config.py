import pytest
import logging
import paramiko
import time
from collections import namedtuple
import pytest_check as check
from conftest import *
from config import *
import re


pytestmark = [pytest.mark.env_name("SNMP_CLI_env"), pytest.mark.cli_dev("shelf_olt")]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bridge_definition = namedtuple('bridge_definition', ['Index', 'config', "result_find", "result_error", 'result_not_find', 'grep'])
bridge_definition.__new__.__defaults__ = (None, "", [], [], [], "")


bridge_definition_DATA = [
 bridge_definition(1, "bridge 1 protocol ieee ageing-time 100 forward-time 30 hello-time 1 max-age 6 max-hops 20 priority 4096", 
 result_find=["bridge 1 protocol ieee" ,
 "bridge 1 ageing-time 100",
 "bridge 1 forward-time 30",
 "bridge 1 hello-time 1",
 "bridge 1 max-age 6",
 "bridge 1 max-hops 20",
 "bridge 1 priority 4096"],grep="bridge"),

 bridge_definition(2, "bridge 1 protocol ieee-vlan-bridge ageing-time 100 forward-time 28 hello-time 2 max-age 7 max-hops 20 priority 8192", 
 result_find=["bridge 1 protocol ieee-vlan-bridge" ,
 "bridge 1 ageing-time 100",
 "bridge 1 forward-time 28",
 "bridge 1 hello-time 2",
 "bridge 1 max-age 7",
 "bridge 1 max-hops 20",
 "bridge 1 priority 8192"], 
 grep="bridge"),

bridge_definition(3, "bridge 1 protocol ieee-vlan-bridge ageing-time 100 forward-time 120 hello-time 2 max-age 7 max-hops 20 priority 8192", 
result_find=["bridge 1 protocol ieee-vlan-bridge" ,
 "bridge 1 ageing-time 100",
 "bridge 1 forward-time 28",
 "bridge 1 hello-time 2",
 "bridge 1 max-age 7",
 "bridge 1 max-hops 20",
 "bridge 1 priority 8192"],result_error =["Problem"],grep="bridge"),

bridge_definition(4, "bridge 1 protocol provider-mstp-edge ageing-time 100 forward-time 30 hello-time 1 max-age 6 max-hops 20 priority 8192", 
result_find=["bridge 1 protocol provider-mstp-edge" ,
 "bridge 1 ageing-time 100",
 "bridge 1 forward-time 30",
 "bridge 1 hello-time 2",
 "bridge 1 max-age 6",
 "bridge 1 max-hops 20",
 "bridge 1 priority 8192"],result_error =["Error code: -1624"],grep="bridge"),

bridge_definition(5, "bridge 1 protocol rstp ageing-time 100 forward-time 30 hello-time 1 max-age 6 max-hops 30 priority 8192", 
result_find=["bridge 1 protocol rstp" ,
 "bridge 1 ageing-time 100",
 "bridge 1 forward-time 30",
 "bridge 1 hello-time 1",
 "bridge 1 max-age 6",
 "bridge 1 max-hops 20",
 "bridge 1 priority 8192"],result_error =["Error code: -1624"],grep="bridge"),

 bridge_definition(5, "bridge 1 protocol rstp ageing-time 100 forward-time 30 hello-time 1 max-age 6 max-hops 20 priority 8192", 
result_find=["bridge 1 protocol rstp" ,
 "bridge 1 ageing-time 100",
 "bridge 1 forward-time 30",
 "bridge 1 hello-time 1",
 "bridge 1 max-age 6",
 "bridge 1 max-hops 20",
 "bridge 1 priority 8192"],grep="bridge"),
 ]

bridge_definition_DELETE = bridge_definition(1, "no bridge 1", 
result_not_find=["bridge 1"],grep= "bridge")

def Bridge_definition(cli_interface_module, data=bridge_definition()): 
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


def test_Bridge_definition(cli_interface_module):
    cli_interface_module.change_to_config() 
    for bridge in bridge_definition_DATA:
        Bridge_definition(cli_interface_module, bridge)
    Bridge_definition(cli_interface_module, bridge_definition_DELETE)












    





    
