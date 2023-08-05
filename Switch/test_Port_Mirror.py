import pytest
import logging
import paramiko
from clilib import CliInterface
import time
from collections import namedtuple
import pytest_check as check
from config import *
from conftest import *
from Switch.test_Bridge_config import Bridge_definition
from Switch.test_Bridge_Group_config import Switch_config

pytestmark = [pytest.mark.env_name("SNMP_CLI_env"), pytest.mark.cli_dev(Test_Target)]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Port_Mirror = namedtuple('Port_Mirror', ['Index', 'config', "result_find", "result_error", 'result_not_find', 'grep', "port"])
Port_Mirror.__new__.__defaults__ = (None, "", [], [], [], "", None)

Port_Mirror_Config_First_Port = [
  Port_Mirror(1, f"mirror both destination interface ge1/{port}", result_error=["Error code: -1625"], grep="mirror"),
  Port_Mirror(2, f"mirror both destination interface ge1/{port+2}", result_find=[f"mirror both destination interface ge1/{port+2}"], grep="mirror"),
  Port_Mirror(2, f"mirror ingress destination interface ge1/{port+2}", result_error=["Error code: -1625"], grep="mirror"),
  Port_Mirror(2, f"mirror egress destination interface ge1/{port+2}", result_error=["Error code: -1625"], grep="mirror"),
  Port_Mirror(2, f"mirror both destination interface ge1/{port+1}", result_find=[f"mirror both destination interface ge1/{port+1}"], grep="mirror"),
  Port_Mirror(2, f"no mirror both ge1/{port+1}", result_not_find=["mirror both"], grep="mirror"),
  Port_Mirror(2, f"mirror egress destination interface ge1/{port+1}", result_find=[f"mirror egress destination interface ge1/{port+1}"], grep="mirror"),
  Port_Mirror(2, f"mirror both destination interface ge1/{port+1}", result_error=["Error code: -1625"], grep="mirror"),
  Port_Mirror(2, f"mirror ingress destination interface ge1/{port+1}", result_error=["Error code: -1625"], grep="mirror"),
  Port_Mirror(2, f"no mirror egress ge1/{port+1}", result_not_find=["mirror both"], grep="mirror"),
  Port_Mirror(2, f"mirror ingress destination interface ge1/{port+1}", result_find=[f"mirror egress destination interface ge1/{port+1}"], grep="mirror"),
  Port_Mirror(2, f"mirror both destination interface ge1/{port+1}", result_error=["Error code: -1625"], grep="mirror"),
  Port_Mirror(2, f"mirror egress destination interface ge1/{port+1}", result_error=["Error code: -1625"], grep="mirror"),
]

Port_Mirror_Config_Second_Port = [
 Port_Mirror(1, f"mirror both destination interface ge1/{port}", result_error=["Error code: -1625"], grep="mirror"),
 Port_Mirror(1, f"mirror both destination interface ge1/{port+2}", result_find=[f"mirror both destination interface ge1/{port+2}"], grep="mirror"),
 Port_Mirror(2, f"mirror ingress destination interface ge1/{port+2}", result_error=["Error code: -1625"], grep="mirror"),
 Port_Mirror(2, f"mirror egress destination interface ge1/{port+2}", result_error=["Error code: -1625"], grep="mirror"),
 Port_Mirror(2, f"mirror both destination interface ge1/{port}", result_find=[f"mirror both destination interface ge1/{port}"], grep="mirror"),
 Port_Mirror(2, f"no mirror both ge1/{port}", result_not_find=["mirror both"], grep="mirror"),
 Port_Mirror(2, f"mirror egress destination interface ge1/{port}", result_find=[f"mirror egress destination interface ge1/{port}"], grep="mirror"),
 Port_Mirror(2, f"mirror both destination interface ge1/{port}", result_error=["Error code: -1625"], grep="mirror"),
 Port_Mirror(2, f"mirror ingress destination interface ge1/{port}", result_error=["Error code: -1625"], grep="mirror"),
 Port_Mirror(2, f"no mirror egress ge1/{port}", result_not_find=["mirror both"], grep="mirror"),
 Port_Mirror(2, f"mirror ingress destination interface ge1/{port}", result_find=[f"mirror egress destination interface ge1/{port}"], grep="mirror"),
 Port_Mirror(2, f"mirror both destination interface ge1/{port}", result_error=["Error code: -1625"], grep="mirror"),
 Port_Mirror(2, f"mirror egress destination interface ge1/{port}", result_error=["Error code: -1625"], grep="mirror"),
]


Port_Mirror_Config_Default = [
  Port_Mirror(1, "no mirror both", result_not_find=["mirror both"], grep="mirror"),
  Port_Mirror(1, "no mirror ingree", result_not_find=["mirror ingree"], grep="mirror"),
  Port_Mirror(1, "no mirror egress", result_not_find=["mirror egress"], grep="mirror"),
]


 
def Port_Mirror_Configuration(cli_interface_module, data=[], method="SET"):  
    logger.info(f'PORT MIRROR TEST DATA ------- > {data.Index} IN METHODE {method}')  
    result_find = data.result_find
    result_error = data.result_error
    result_not_find = data.result_not_find
    grep = data.grep
    detail_result = cli_interface_module.exec(data.config) 
    detail_result = '\n'.join(detail_result.split('\n')[1:-1])  
    if len(result_find) != 0:
        for f in result_find:
            result = get_result(cli_interface_module, f"{grep}")
            assert (result.find(f)!=-1),f"NOT EXIST {f} in config"
    if len(result_error) != 0:
        for error in result_error:
            assert (detail_result.find(error)!=-1),f"APPLY ERROR DATA"
    if len(result_not_find) != 0:
        for nf in result_not_find:
            result = get_result(cli_interface_module, f"{grep}")
            assert (result.find(nf)==-1),f"FIND {data.config} IN CONFIG OF SYSTEM AND NOT TO BE CLEARED"

def test_Port_Mirror_Configuration(cli_interface_module):
    for port in range(1,2):
        for i in range(len(Port_Mirror_Config_Second_Port)):
            if 1 <= port <=8 :
                cli_interface_module.exec(f"interface ge1/{port}") 
                Port_Mirror_Configuration(cli_interface_module, Port_Mirror_Config_First_Port[i]._replace(port=port), "SET")
                cli_interface_module.exec(f"interface ge1/{port+1}") 
                Port_Mirror_Configuration(cli_interface_module, Port_Mirror_Config_Second_Port[i]._replace(port=port), "SET")
            else:    
                cli_interface_module.exec(f"interface gpon-olt1/{port-8}") 
                Port_Mirror_Configuration(cli_interface_module, Port_Mirror_Config_First_Port[i]._replace(port=port), "SET")
                cli_interface_module.exec(f"interface gpon-olt1/{port+1-8}") 
                Port_Mirror_Configuration(cli_interface_module, Port_Mirror_Config_Second_Port[i]._replace(port=port), "SET")

    for port in range(1,4):
        if 1 <= port <=8 :
            cli_interface_module.exec(f"interface ge1/{port}") 
        else:    
            cli_interface_module.exec(f"interface gpon-olt1/{port-8}") 
        for port_mirror in Port_Mirror_Config_Default:
            Port_Storm_Control_Config(cli_interface_module, port_mirror, "DEFAULT")
      





