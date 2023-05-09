import pytest
import logging
import paramiko
from clilib import CliInterface
import time
from collections import namedtuple
import pytest_check as check
from schema import Use
from config_service import *


pytestmark = [pytest.mark.env_name("SNMP_CLI_env"), pytest.mark.cli_dev("snmp_cli")]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def repeat_config(cli_interface_module,config=None, begin=None, finish=None, parameter=None):
    for i in range(begin,finish):
        config = config.replace(parameter, f" {i} ")
        parameter = f" {i} "
        cli_interface_module.exec(config)
        logger.info(f"pass interface set step with {config}")
        result = str(cli_interface_module.exec(f"show running-config interface | grep {config}"))
        check.is_in(config, result, msg= f"NOT EXIST THIS CONFIG {config} IN INTERFACE AFTER SET")

def set_and_check_config_interface(cli_interface_module,config_array, index_port, index_repeat=None):
    command = "interface "+index_port
    cli_interface_module.exec(command)
    for i in range(0,len(config_array)):
        cli_interface_module.exec(f"{config_array[i]}")
        logger.info(f"pass interface set step with {config_array[i]}")
        result = str(cli_interface_module.exec(f"show running-config interface | grep {config_array[i]}"))
        check.is_in(config_array[i], result, msg= f"NOT EXIST THIS CONFIG {config_array[i]} IN INTERFACE AFTER SET {index_port}")

def set_and_check_config_total(cli_interface_module,config_array):
    for i in range(0,len(config_array)):
        cli_interface_module.exec(f"{config_array[i]}")
        logger.info(f"pass total set step with {config_array[i]}")
        result = str(cli_interface_module.exec(f"show running-config | grep {config_array[i]}"))
        check.is_in(config_array[i], result, msg= f"not exist this config {config_array[i]} in interface total config")

def Service_1(cli_interface_module, data_conf=config_Service_1):
    cli_interface_module.change_to_config()   
    cli_interface_module.exec("gpon")
    cli_interface_module.exec("exit")
    set_and_check_config_interface(cli_interface_module, [data_conf['gpon-olt1/1'][0]], "gpon-olt1/1")
    set_and_check_config_interface(cli_interface_module, [data_conf['gpon-olt1/2'][0]], "gpon-olt1/2")
    cli_interface_module.exec("exit")
    for i in range(0,4):
        set_and_check_config_interface(cli_interface_module, data_conf['gpon-onu1'], f"gpon-onu1/1:{i+1}")
        repeat_config(cli_interface_module, data_conf['gpon-onu1_repeat'][0], 111, 116, " vlan ")
        repeat_config(cli_interface_module, data_conf['gpon-onu1_repeat'][1], 111, 116, " vlan ")
    # for i in range(0,6):
    #     set_and_check_config_interface(cli_interface_module, data_conf['gpon-onu1'], f"gpon-onu1/2:{i+1}")
    #     repeat_config(cli_interface_module, data_conf['gpon-onu1_repeat'][0], 117, 222, data_conf['gpon-onu1_repeat'][0].vlan)
    #     repeat_config(cli_interface_module, data_conf['gpon-onu1_repeat'][1], 117, 222, data_conf['gpon-onu1_repeat'][0].vlan)
    # cli_interface_module.exec("exit")
    # set_and_check_config_total(cli_interface_module, data_conf['total'])
    # set_and_check_config_interface(cli_interface_module, data_conf['gpon-olt1/1'][1:], "gpon-olt1/1")
    # set_and_check_config_interface(cli_interface_module, data_conf['gpon-olt1/2'][1:], "gpon-olt1/2")
    # set_and_check_config_interface(cli_interface_module, data_conf['ge1/1'], "ge1/1")



def test_Service(cli_interface_module):
    Service_1(cli_interface_module,config_Service_1)
    



       