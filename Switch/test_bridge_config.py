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

Bridge = namedtuple('Bridge', ['bridgeId', 'bridgeProtocol', 'ageingTime', 'forwardTime', 'helloTime', 'maxAge',
                               'maxHops', 'priority', 'id', 'result'])
Bridge.__new__.__defaults__ = (1, "IEEE_VLAN_BRIDGE", 100, 15, 2, 20, 20, 32768, 1, "Pass", 1, 1, None)
BRIDGE_DATA = [
    Bridge(1, 'ieee', 100, 30, 1, 6, priority=4096),
    # Bridge(1, 'ieee_vlan_bridge', 1000, 29, 2, 7, priority=8192),
    # Bridge(1, 'nstp', 100, 30, maxAge=6, maxHops=1, priority=12288),
    # Bridge(1, 'mstpring', 1000, 29, maxAge=7, maxHops=20, priority=16384),
    # Bridge(1, 'rpvstp', 100, priority=20480),
    # Bridge(1, 'rstp', 1000, 29, 2, 7, priority=24576),
    # Bridge(1, 'rstp_ring', 100, 30, 1, 6, priority=28672),
    # Bridge(1, 'rstp_vlan_bridge', 1000, 29, 2, 7, priority=32768),
    # Bridge(1, 'rstp_vlan_bridge_ring', 100, 30, 1, 6, priority=36864),
    # Bridge(1, 'provider_mstp', 1000, 29, maxAge=7, maxHops=35, priority=40960),
    # Bridge(1, 'provider_mstp_edge', 100, 30, maxAge=6, maxHops=39, priority=45056),
    # Bridge(1, 'provider_rstp', 1000, 29, 2, 7, priority=49152),
    # Bridge(1, 'provider_rstp_edge', 1000, 29, 2, 7, priority=53248)
]


def bridge_cli(cli_interface_module, data=Bridge(), method="Post"):

    config_of_bridge = [f"bridge 1 protocol {data.bridgeProtocol}",
                        f"bridge 1 ageing-time {data.ageingTime}",
                        f"bridge 1 forward-time {data.forwardTime}",
                        f"bridge 1 hello-time {data.helloTime}",
                        f"bridge 1 max-age {data.maxAge}",
                        f"bridge 1 priority {data.priority}"]

    cli_interface_module.change_to_config()  
    if method == "Post": 
        cli_interface_module.exec(f"bridge 1 protocol {data.bridgeProtocol} ageing-time {data.ageingTime} forward-time {data.forwardTime} hello-time {data.helloTime} max-age {data.maxAge} priority {data.priority}") 
        cli_interface_module.exec("show running-config")
        result = str(cli_interface_module.exec(f"show running-config | grep bridge"))
        result = '\n'.join(result.split('\n')[1:-1])
        for i in range(0,len(config_of_bridge)):
            assert (result.find(config_of_bridge[i])!=-1),f"NOT EXIST THIS CONFIG {config_of_bridge[i]}"
            #check.is_in(config_of_bridge[i], result, msg= f"not exist this config {config_of_bridge[i]}")
    elif method == "Delete":
        cli_interface_module.exec(f"no bridge 1 protocol {data.bridgeProtocol} ageing-time {data.ageingTime} forward-time {data.forwardTime} hello-time {data.helloTime} max-age {data.maxAge} priority {data.priority}") 
        cli_interface_module.exec("show running-config")
        result = str(cli_interface_module.exec(f"show running-config | grep bridge 1"))
        result = '\n'.join(result.split('\n')[1:-1])
        assert (result.find("bridge 1")==-1),f"NOT EXIST THIS CONFIG Bridge"
        #check.is_not_in(config_of_bridge[i], result, msg= f" exist this config {config_of_bridge[i]}")  

# @pytest.mark.parametrize('data', BRIDGE_DATA)
def test_bridge_cli(cli_interface_module):
    for data in BRIDGE_DATA:
        bridge_cli(cli_interface_module, data, "Post")
        # bridge_cli(cli_interface_module, data, "Delete")


    





    
