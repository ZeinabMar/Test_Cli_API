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

pytestmark = [pytest.mark.env_name("SNMP_CLI_env"), pytest.mark.cli_dev("shelf_olt")]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Port_Storm = namedtuple('Port_Storm', ['Index', 'config', "result_find", "result_error", 'result_not_find', 'grep'])
Port_Storm.__new__.__defaults__ = (None, "", [], [], [], "")

Port_Storm_Control = [
  Port_Storm(1, "storm-control broadcast level 14.5", result_find=["storm-control broadcast level 14.500000"], grep="storm-control"),
  Port_Storm(2, "storm-control dlf level 25", result_find=["storm-control dlf level 25.000000"], grep="storm-control"),
  Port_Storm(3, "storm-control broadcast level 135", result_find=["storm-control broadcast level 14.500000", "storm-control dlf level 25.000000"], 
  result_error=["Invalid level"], grep="storm-control"),

  Port_Storm(4, "storm-control multicast level 135", result_find=["storm-control broadcast level 14.500000", "storm-control dlf level 25.000000"], 
  result_error=["Invalid level"], result_not_find=["storm-control multicast level"],grep="storm-control"),

  Port_Storm(5, "storm-control multicast level 47", 
  result_find=["storm-control multicast level 47.000000","storm-control broadcast level 14.500000", "storm-control dlf level 25.000000"], 
  grep="storm-control"),

  Port_Storm(6, "storm-control dlf level 145", 
  result_find=["storm-control multicast level 47.000000","storm-control broadcast level 14.500000", "storm-control dlf level 25.000000"], 
  result_error=["Invalid level"], grep="storm-control"),
]

Port_Storm_Control_Default = [
  Port_Storm(1, "no storm-control multicast", result_not_find=["storm-control multicast"], grep="storm-control"),
  Port_Storm(1, "no storm-control dlf", result_not_find=["storm-control dlf"], grep="storm-control"),
  Port_Storm(1, "no storm-control broadcast", result_not_find=["storm-control broadcast"], grep="storm-control"),
]


 
def Port_Storm_Control_Config(cli_interface_module, data=[], method="SET"):  
    logger.info(f'PORT STORM CONTROL TEST DATA ------- > {data.Index} IN METHODE {method}')  
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

def test_Port_Storm_Control_Config(cli_interface_module):
    cli_interface_module.change_to_config() 
    Bridge_definition(cli_interface_module, bridge_custom[0])
    for port in range(1,2):
        if 1 <= port <=8 :
            cli_interface_module.exec(f"interface ge1/{port}") 
        else:    
            cli_interface_module.exec(f"interface gpon-olt1/{port-8}") 
        Switch_config(cli_interface_module, Switch_Enable)
        for port_storm in Port_Storm_Control:
            Port_Storm_Control_Config(cli_interface_module, port_storm, "SET")
        for port_storm in Port_Storm_Control_Default:
            Port_Storm_Control_Config(cli_interface_module, port_storm, "DEFAULT")
        Switch_config(cli_interface_module, Switch_Disable)
    cli_interface_module.exec("exit") 
    Bridge_definition(cli_interface_module, bridge_definition_DELETE)        
            





