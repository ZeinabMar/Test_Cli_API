import pytest
import logging
import paramiko
from clilib import CliInterface
import time
from collections import namedtuple
import pytest_check as check
from schema import Use
from config import *

Test_Target = 'snmp_cli'

pytestmark = [pytest.mark.env_name("SNMP_CLI_env"), pytest.mark.cli_dev(Test_Target)]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Qos_policy = namedtuple('Qos_policy', ['Index', 'config', "result_find", "result_error", 'result_not_find', 'grep'])
Qos_policy.__new__.__defaults__ = (None, "", [], [], [], "")


Qos_policy_DATA = [
 Qos_policy(1, "policy-map policy class B avg 2000 burst 20000 exceed-burst 20000 exceed-action drop bucket cbs", 
 result_find=["policy-map policy class B avg 2000 burst 20000 exceed-burst 20000 exceed-action drop bucket cbs"], grep="policy-map"),

 Qos_policy(2, "policy-map policy class C avg 2000 burst 20000 exceed-burst 20000 exceed-action drop bucket cbs",
 result_find=["policy-map policy class C avg 2000 burst 20000 exceed-burst 20000 exceed-action drop bucket cbs"], grep="policy-map"),

 Qos_policy(3, "policy-map policy class B avg 222 burst 222 exceed-burst 222 exceed-action drop bucket cbs", 
 result_find=["policy-map policy class B avg 222 burst 222 exceed-burst 222 exceed-action drop bucket cbs"],grep="policy-map"),

Qos_policy(4, "policy-map policy class B avg 222 burst 1000001 exceed-burst 20000 exceed-action drop bucket cbs", 
result_find=["policy-map policy class B avg 222 burst 222 exceed-burst 222 exceed-action drop bucket cbs"],
result_error=["Invalid burst"], grep="policy-map"),

Qos_policy(5, "policy-map policy class B avg 222 burst 100000 exceed-burst 2000000 exceed-action drop bucket cbs", 
result_find=["policy-map policy class B avg 222 burst 222 exceed-burst 222 exceed-action drop bucket cbs"],
result_error=["Invalid burst"], grep="policy-map"),

Qos_policy(6, "policy-map policy class B avg 20000000 burst 20000 exceed-burst 20000 exceed-action drop bucket cbs", 
result_find=["policy-map policy class B avg 222 burst 222 exceed-burst 222 exceed-action drop bucket cbs"],
result_error=["Invalid avg"], grep="policy-map"),

Qos_policy(7, "no policy-map policy class B avg 222 burst 222 exceed-burst 222 exceed-action drop bucket cbs", 
result_not_find=["policy-map policy class B avg 2000 burst 20000 exceed-burst 20000 exceed-action drop bucket cbs"],
grep="policy-map"),

Qos_policy(8, "no policy-map policy class C avg 2000 burst 20000 exceed-burst 20000 exceed-action drop bucket cbs", 
result_not_find=["policy-map policy class C avg 2000 burst 20000 exceed-burst 20000 exceed-action drop bucket cbs"],
grep="policy-map"),
]


def Qos_Policy_configuration(cli_interface_module, data=Qos_policy()): 

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

def test_Qos_Policy_configuration(cli_interface_module):
    cli_interface_module.change_to_config() 
    for qos_policy in Qos_policy_DATA:
        Qos_Policy_configuration(cli_interface_module, qos_policy)
        
