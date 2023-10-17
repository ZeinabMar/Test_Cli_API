import pytest
import logging
import paramiko
from clilib import CliInterface
import time
from collections import namedtuple
import pytest_check as check
from conftest import *
from config import *
from Switch.test_Bridge_config import Bridge_definition
from Switch.test_Vlan_config import vlan_management
from Switch.test_Qos_management import Qos_Management
from Switch.test_Qos_class_definition import Qos_class_definition


pytestmark = [pytest.mark.env_name("SNMP_CLI_env"), pytest.mark.cli_dev(Test_Target)]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Qos_policy = namedtuple('Qos_policy', ['Index', 'config', "result_find", "result_error", 'result_not_find', 'grep'])
Qos_policy.__new__.__defaults__ = (None, "", [], [], [], "")


Qos_policy_DATA = [
[
Qos_policy(1, "policy-map policy class B mode allow", result_find=["policy-map policy class B mode allow"], grep="policy-map"),
 Qos_policy(2, "policy-map policy class B count-type byte-based color aware rate-type two-rate peak 1000 avg 1000 burst 1000 exceed-burst 1000 act drop", 
 result_find=["policy-map policy class B count-type byte-based color aware rate-type two-rate peak 1000 avg 1000 burst 1000 exceed-burst 1000 act drop"], grep="policy-map"),
 Qos_policy(3, "policy-map policy class B set cos 5", result_find=["policy-map policy class B set cos 5"], grep="policy-map"),
 Qos_policy(4, "no policy-map policy class B set cos 5", result_not_find=["policy-map policy class B set cos 5"], grep="policy-map"),

 Qos_policy(5, "policy-map policy class B set ip-dscp 64", result_error=["Problem"], result_not_find=["policy-map policy class B set ip-dscp 64"], grep="policy-map"),
 Qos_policy(6, "policy-map policy class B set ip-precedence 8", result_error=["Problem"], result_not_find=["policy-map policy class B set ip-precedence 8"], grep="policy-map"),
  Qos_policy(7, "policy-map policy class B set ip-precedence 26", result_error=["Problem"], result_not_find=["policy-map policy class B set ip-precedence 26"], grep="policy-map"),

 Qos_policy(8, "policy-map policy class B set mirror-to-port ge1/26", result_error=["Error code: -1632"], result_not_find=["policy-map policy class B set mirror-to-port"], grep="policy-map"),
 Qos_policy(9, "policy-map policy class B set vlan 4500", result_error=["Problem"], result_not_find=["policy-map policy class B set redirect-to-point"], grep="policy-map"),
 Qos_policy(10, "policy-map policy class B set vlan 1200", result_find=["policy-map policy class B set vlan 1200"], grep="policy-map"),
 Qos_policy(11, "no policy-map policy class B set vlan 1200", result_not_find=["policy-map policy class B set vlan"], grep="policy-map"),
 Qos_policy(12, "policy-map policy class B set redirect-to-port ge1/1", result_find=["policy-map policy class B set redirect-to-port ge1/1"], grep="policy-map"),
],

[
Qos_policy(1, "policy-map policy class C mode deny", result_find=["policy-map policy class C mode deny"], grep="policy-map"),

 Qos_policy(1, "policy-map policy class C count-type byte-based color aware rate-type two-rate peak 1000 avg 1000 burst 100000000 exceed-burst 1000 act drop", 
 result_error=["Problem"], result_not_find=["policy-map policy1 class C count-type byte-based"], grep="policy-map"),

 Qos_policy(1, "policy-map policy class C count-type byte-based color aware rate-type two-rate peak 1000 avg 10000000000000 burst 1000 exceed-burst 1000 act drop", 
 result_error=["Problem"], result_not_find=["policy-map policy1 class C count-type byte-based"], grep="policy-map"),

 Qos_policy(1, "policy-map policy class C count-type byte-based color aware rate-type two-rate peak 1000 avg 1000 burst 1000 exceed-burst 1000 act drop", 
 result_find=["policy-map policy class C count-type byte-based color aware rate-type two-rate peak 1000 avg 1000 burst 1000 exceed-burst 1000 act drop"], grep="policy-map"),
 
 Qos_policy(1, "policy-map policy class C set ip-dscp 12 priority 5", result_find=["policy-map policy class C set ip-dscp 12"], grep="policy-map"),
 Qos_policy(1, "no policy-map policy class C set ip-dscp 12", result_not_find=["policy-map policy class C set ip-dscp"], grep="policy-map"),
 Qos_policy(1, "policy-map policy class C set vlan 25 priority 8", result_error=["Problem"], result_not_find=["policy-map policy class C set vlan 25"], grep="policy-map"),
 Qos_policy(1, "policy-map policy class C set vlan 25 priority 5", result_find=["policy-map policy class C set vlan 25 priority 5"], grep="policy-map"),
 Qos_policy(1, "no policy-map policy class C mode deny", result_not_find=["policy-map policy class C mode"], grep="policy-map"),
 ],

 [Qos_policy(1, "policy-map policy1 class C set ip-dscp 12", result_find=["policy-map policy1 class C set ip-dscp 12"], grep="policy-map"),
 Qos_policy(1, "policy-map policy1 class C count-type byte-based color aware rate-type two-rate peak 1000 avg 1000 burst 1000 exceed-burst 1000 act drop", 
 result_find=["policy-map policy1 class C count-type byte-based color aware rate-type two-rate peak 1000 avg 1000 burst 1000 exceed-burst 1000 act drop"], grep="policy-map"),

]
 
]

Qos_policy_DATA_Delete = [
     [Qos_policy(1, "no policy-map policy class C count-type byte-based color aware rate-type two-rate peak 1000 avg 1000 burst 1000 exceed-burst 1000 act drop", 
     result_not_find=["policy-map policy1 class C count-type byte-based"], grep="policy-map"),
     Qos_policy(1, "no policy-map policy class B", result_not_find=["policy-map policy class B"], grep="policy-map")],
     [Qos_policy(2, "no policy-map policy1 class C", result_not_find=["policy-map policy1 class C"], grep="policy-map")],
]


def Qos_Policy_configuration(cli_interface_module, DATA=[Qos_policy()]): 
    for data in DATA:
        result_find = data.result_find
        result_error = data.result_error
        result_not_find = data.result_not_find
        grep = data.grep

        detail_result = cli_interface_module.exec(data.config) 
        detail_result = '\n'.join(detail_result.split('\n')[1:])  
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

def test_Qos_Policy_configuration(cli_interface_module):
    cli_interface_module.change_to_config() 
    Bridge_definition(cli_interface_module, bridge_service_custom[0])
    for vlan_custom in Vlan_Custom:
        vlan_management(cli_interface_module, vlan_custom)
    Qos_Management(cli_interface_module, Qos_Enable)    
    for qos_class in Qos_Class_Config:
        Qos_class_definition(cli_interface_module, qos_class)

    for qos_policy in Qos_policy_DATA:
        Qos_Policy_configuration(cli_interface_module, qos_policy)

    for qos_policy_del in Qos_policy_DATA_Delete:
        Qos_Policy_configuration(cli_interface_module, qos_policy_del)

    for qos_class in Qos_Class_Config_Delete:
        Qos_class_definition(cli_interface_module, qos_class)
    Qos_Management(cli_interface_module, Qos_Disable)    
    for vlan_custom in Vlan_Custom_DELETE:
        vlan_management(cli_interface_module, vlan_custom)
    Bridge_definition(cli_interface_module, bridge_definition_DELETE) 