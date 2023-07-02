import pytest
import logging
import paramiko
from clilib import CliInterface
import time
from collections import namedtuple
import pytest_check as check
# from schema import Use
from config import *
import re

Test_Target = 'snmp_cli'

pytestmark = [pytest.mark.env_name("SNMP_CLI_env"), pytest.mark.cli_dev(Test_Target)]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bridge_definition = namedtuple('bridge_definition', ['Index', 'config', "result_find", "result_error", 'result_not_find', 'grep'])
bridge_definition.__new__.__defaults__ = (None, "", [], [], [], "")
# BRIDGE_DATA = [
#     Bridge(2, 'ieee', 100, 30, 1, 6, priority=4096, result="Fail"),
#     # Bridge(1, 'ieee_vlan_bridge', 1000, 29, 2, 7, priority=8192),
#     # Bridge(1, 'nstp', 100, 30, maxAge=6, maxHops=1, priority=12288),
#     # Bridge(1, 'mstpring', 1000, 29, maxAge=7, maxHops=20, priority=16384),
#     # Bridge(1, 'rpvstp', 100, priority=20480),
#     # Bridge(1, 'rstp', 1000, 29, 2, 7, priority=24576),
#     # Bridge(1, 'rstp_ring', 100, 30, 1, 6, priority=28672),
#     # Bridge(1, 'rstp_vlan_bridge', 1000, 29, 2, 7, priority=32768),
#     # Bridge(1, 'rstp_vlan_bridge_ring', 100, 30, 1, 6, priority=36864),
#     # Bridge(1, 'provider_mstp', 1000, 29, maxAge=7, maxHops=35, priority=40960),
#     # Bridge(1, 'provider_mstp_edge', 100, 30, maxAge=6, maxHops=39, priority=45056),
#     # Bridge(1, 'provider_rstp', 1000, 29, 2, 7, priority=49152),
#     # Bridge(1, 'provider_rstp_edge', 1000, 29, 2, 7, priority=53248)
# ]

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
 ]

bridge_definition_DELETE = [
bridge_definition(1, "no bridge 1", 
result_not_find=["bridge 1"],grep= "bridge")]

def bridge_definition(cli_interface_module, data=bridge_definition()): 
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

def test_bridge_definition(cli_interface_module):
    cli_interface_module.change_to_config() 
    for bridge in bridge_definition_DATA:
        bridge_definition(cli_interface_module, bridge)
    bridge_definition(cli_interface_module, bridge_definition_DELETE[0])












    





    
