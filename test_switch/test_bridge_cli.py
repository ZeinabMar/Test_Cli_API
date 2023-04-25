import pytest
import logging
import paramiko
from clilib import CliInterface
import time
from collections import namedtuple
import pytest_check as check
from schema import Use

Test_Target = 'PS6x_card'

pytestmark = [pytest.mark.env_name("NP_env"), pytest.mark.cli_dev(Test_Target)]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Bridge = namedtuple('Bridge', ['bridgeId', 'bridgeProtocol', 'ageingTime', 'forwardTime', 'helloTime', 'maxAge',
                               'maxHops', 'priority', 'id', 'result'])
Bridge.__new__.__defaults__ = (1, "IEEE_VLAN_BRIDGE", 100, 15, 2, 20, 20, 32768, 1, "Pass", 1, 1, None)
BRIDGE_DATA = (
    Bridge(1, 'IEEE', 100, 30, 1, 6, priority=4096),
    Bridge(1, 'IEEE_VLAN_BRIDGE', 1000, 29, 2, 7, priority=8192),
    Bridge(1, 'MSTP', 100, 30, maxAge=6, maxHops=1, priority=12288),
    Bridge(1, 'MSTPRING', 1000, 29, maxAge=7, maxHops=20, priority=16384),
    Bridge(1, 'RPVSTP', 100, priority=20480),
    Bridge(1, 'RSTP', 1000, 29, 2, 7, priority=24576),
    Bridge(1, 'RSTP_RING', 100, 30, 1, 6, priority=28672),
    Bridge(1, 'RSTP_VLAN_BRIDGE', 1000, 29, 2, 7, priority=32768),
    Bridge(1, 'RSTP_VLAN_BRIDGE_RING', 100, 30, 1, 6, priority=36864),
    Bridge(1, 'PROVIDER_MSTP', 1000, 29, maxAge=7, maxHops=35, priority=40960),
    Bridge(1, 'PROVIDER_MSTP_EDGE', 100, 30, maxAge=6, maxHops=39, priority=45056),
    Bridge(1, 'PROVIDER_RSTP', 1000, 29, 2, 7, priority=49152),
    Bridge(1, 'PROVIDER_RSTP_EDGE', 1000, 29, 2, 7, priority=53248)
)


def bridge_cli(cli_interface_module, data=Bridge()):

    config_of_bridge = [f"bridge 1 protocol {data.protocol}",
                        f"bridge 1 protocol {data.ageingTime}",
                        f"bridge 1 protocol {data.forwardTime}",
                        f"bridge 1 protocol {data.helloTime}",
                        f"bridge 1 protocol {data.maxAge}",
                        f"bridge 1 protocol {data.priority}"]

    cli_interface_module.change_to_config()   
    cli_interface_module.exec(f"bridge 1 protocol {data.protocol} ageing-time {data.ageingTime} forward-time {data.forwardTime} hello-time {data.helloTime} max-age {data.maxAge} priority {data.priority}") 
    cli_interface_module.exec("show running-config")
    result = str(cli_interface_module.exec("A"))  
    for i in range(0,len(config_of_bridge_vlan)):
        check.is_in(config_of_bridge_vlan[i], result, msg= f"not exist this config {config_of_bridge[i]}")

    cli_interface_module.exec(f"no bridge 1 protocol {data.protocol} ageing-time {data.ageingTime} forward-time {data.forwardTime} hello-time {data.helloTime} max-age {data.maxAge} priority {data.priority}") 
    cli_interface_module.exec("show running-config")
    result = str(cli_interface_module.exec("A"))    
    for i in range(0,len(config_of_bridge_vlan)):
        check.is_not_in(config_of_bridge_vlan[i], result, msg= f"not exist this config {config_of_bridge[i]}")  

def test_bridge_cli(cli_interface_module):
    bridge_cli(cli_interface_module, BRIDGE_DATA[0])


    





    
