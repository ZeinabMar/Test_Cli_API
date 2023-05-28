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

Vlan = namedtuple('Vlan', ['vlanId','vlanBridgeId', 'vlanTypeId', 'vlanState'])
Vlan.__new__.__defaults__ = (100, 'CUSTOMER', 1, 1, 'Pass', 1, 1, None)

VLAN_DATA = [
    Vlan(10, 1, "customer", "enable"),
    Vlan(11, 1, "customer", "enable"),
    Vlan(110, 1, "service-point-point", "enable"),
    Vlan(111, 1, "service-rooted-multipoint", "enable"),
]


def vlan_config(cli_interface_module, data=Vlan(), method="SET"):

    config_of_vlan_set = config_of_vlan_check = f"vlan {data.vlanId} bridge {data.vlanBridgeId} type {data.vlanTypeId} state {data.vlanState}"
    cli_interface_module.change_to_config()   

    if method == "SET":
        cli_interface_module.exec(config_of_vlan_set) 
        result = str(cli_interface_module.exec(f"show running-config | grep {config_of_vlan_check}"))
        result = '\n'.join(result.split('\n')[1:-1])
        assert (result.find(config_of_vlan_check)!=-1),f"NOT EXIST THIS CONFIG {config_of_vlan_set}"
            #check.is_in(config_of_bridge[i], result, msg= f"not exist this config {config_of_bridge[i]}")
    else :
        cli_interface_module.exec(f"no {config_of_vlan_set}") 
        result = str(cli_interface_module.exec(f"show running-config | grep vlan {data.vlanId}"))
        result = '\n'.join(result.split('\n')[1:-1])
        assert (result.find("vlan {data.vlanId}")==-1),f"NOT EXIST THIS CONFIG VLAN"
        #check.is_not_in(config_of_bridge[i], result, msg= f" exist this config {config_of_bridge[i]}")  

# @pytest.mark.parametrize('data', BRIDGE_DATA)
def test_vlan_config(cli_interface_module):
    for data in VLAN_DATA:
        vlan_config(cli_interface_module, data, "SET")
        vlan_config(cli_interface_module, data, "DELETE")