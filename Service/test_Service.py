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
        result = '\n'.join(result.split('\n')[1:-1])
        check.is_in(config, result, msg= f"NOT EXIST THIS CONFIG {config} IN INTERFACE AFTER SET")

def replacement(cli_interface_module, config=None, parameter=None, value_param=None):
    config = config.replace(parameter, f" {value_param} ")
    cli_interface_module.exec(config)
    logger.info(f"pass interface set step with {config}")
    result = str(cli_interface_module.exec(f"show running-config interface | grep {config}"))
    result = '\n'.join(result.split('\n')[1:-1])
    check.is_in(config, result, msg= f"NOT EXIST THIS CONFIG {config} IN INTERFACE AFTER SET")


def set_and_check_config_interface(cli_interface_module,config_array, index_port):
    command = "interface "+index_port
    cli_interface_module.exec(command)
    for i in range(0,len(config_array)):
        cli_interface_module.exec(f"{config_array[i]}")
        logger.info(f"pass interface set step with {config_array[i]}")
        result = str(cli_interface_module.exec(f"show running-config interface | grep {config_array[i]}"))
        result = '\n'.join(result.split('\n')[1:-1])
        assert (result.find(config_array[i])!=-1),f"NOT EXIST THIS CONFIG {config_array[i]} IN INTERFACE AFTER SET {index_port}"
        # check.is_in(config_array[i], result, msg= f"NOT EXIST THIS CONFIG {config_array[i]} IN INTERFACE AFTER SET {index_port}")

def set_and_check_config_total(cli_interface_module,config_array):
    for i in range(0,len(config_array)):
        cli_interface_module.exec(f"{config_array[i]}")
        logger.info(f"pass total set step with {config_array[i]}")
        result = str(cli_interface_module.exec(f"show running-config | grep {config_array[i]}"))
        result = '\n'.join(result.split('\n')[1:-1])
        assert (result.find(config_array[i])!=-1),f"NOT EXIST THIS CONFIG {config_array[i]} IN INTERFACE AFTER SET"
        # check.is_in(config_array[i], result, msg= f"not exist this config {config_array[i]} in interface total config")

def Service_1(cli_interface_module, data_conf=config_Service_1):
    cli_interface_module.change_to_config()   
    cli_interface_module.exec("gpon")
    set_and_check_config_total(cli_interface_module, data_conf['gpon'])
    cli_interface_module.exec("exit")
    set_and_check_config_interface(cli_interface_module, [data_conf['gpon-olt1'][0]], "gpon-olt1/1")
    set_and_check_config_interface(cli_interface_module, [data_conf['gpon-olt1'][0]], "gpon-olt1/2")
    cli_interface_module.exec("exit")
    
    vlan_onu1_1 = [111, 112, 113, 114,115, 116]
    for i in range(0,5):
        set_and_check_config_interface(cli_interface_module, data_conf['gpon-onu1'][:2], f"gpon-onu1/1:{i+1}")
        replacement(cli_interface_module, data_conf['gpon-onu1'][2], " vlan ", vlan_onu1_1[i])
        replacement(cli_interface_module, data_conf['gpon-onu1'][3], " vlan ", vlan_onu1_1[i])
    vlan_onu1_2 = [117, 118, 119, 220, 221, 222]
    # for i in range(0,5):
    #     set_and_check_config_interface(cli_interface_module, data_conf['gpon-onu1'][:2], f"gpon-onu1/2:{i+1}")
    #     replacement(cli_interface_module, data_conf['gpon-onu1'][2], " vlan ", vlan_onu1_2[i])
    #     replacement(cli_interface_module, data_conf['gpon-onu1'][3], " vlan ", vlan_onu1_2[i])

    cli_interface_module.exec("exit")
    set_and_check_config_total(cli_interface_module, data_conf['total'])
    set_and_check_config_interface(cli_interface_module, data_conf['gpon-olt1'][1:], "gpon-olt1/1")
    set_and_check_config_interface(cli_interface_module, data_conf['gpon-olt1'][1:], "gpon-olt1/2")
    set_and_check_config_interface(cli_interface_module, data_conf['ge1/1'], "ge1/1")

def Service_2(cli_interface_module, data_conf=config_Service_2):
    cli_interface_module.change_to_config()   
    cli_interface_module.exec("gpon")
    set_and_check_config_total(cli_interface_module, data_conf['gpon'])
    cli_interface_module.exec("exit")
    set_and_check_config_interface(cli_interface_module, [data_conf['gpon-olt1'][0]], "gpon-olt1/1")
    set_and_check_config_interface(cli_interface_module, [data_conf['gpon-olt1'][0]], "gpon-olt1/2")
    cli_interface_module.exec("exit")
    vlan_onu1_1 = [111, 112, 113, 114,115, 116]
    for i in range(0,1):
        set_and_check_config_interface(cli_interface_module, data_conf['gpon-onu1'][:2], f"gpon-onu1/1:{i+1}")
        replacement(cli_interface_module, data_conf['gpon-onu1'][2], " vlan ", vlan_onu1_1[i])
        replacement(cli_interface_module, data_conf['gpon-onu1'][3], " vlan ", vlan_onu1_1[i])
    vlan_onu1_2 = [117, 118, 119, 220, 221, 222]
    for i in range(0,6):
        set_and_check_config_interface(cli_interface_module, data_conf['gpon-onu1'][:2], f"gpon-onu1/2:{i+1}")
        replacement(cli_interface_module, data_conf['gpon-onu1'][2], " vlan ", vlan_onu1_2[i])
        replacement(cli_interface_module, data_conf['gpon-onu1'][3], " vlan ", vlan_onu1_2[i])
    set_and_check_config_total(cli_interface_module, data_conf['total'])
    set_and_check_config_interface(cli_interface_module, data_conf['gpon-olt1'][1:], "gpon-olt1/1")
    set_and_check_config_interface(cli_interface_module, data_conf['gpon-olt1'][1:], "gpon-olt1/2")
    set_and_check_config_interface(cli_interface_module, data_conf['ge1/1'], "ge1/1")
    set_and_check_config_interface(cli_interface_module, data_conf['ge1/2'], "ge1/2")


def Service_3(cli_interface_module, data_conf=config_Service_3):
    cli_interface_module.change_to_config()   
    cli_interface_module.exec("gpon")
    set_and_check_config_total(cli_interface_module, data_conf['gpon'])
    cli_interface_module.exec("exit")
    set_and_check_config_interface(cli_interface_module, [data_conf['gpon-olt1'][0]], "gpon-olt1/1")
    set_and_check_config_interface(cli_interface_module, [data_conf['gpon-olt1'][0]], "gpon-olt1/2")
    cli_interface_module.exec("exit")
    vlan_onu1_1 = [111, 112, 113, 114,115, 116]
    for i in range(0,1):
        set_and_check_config_interface(cli_interface_module, data_conf['gpon-onu1'][:2], f"gpon-onu1/1:{i+1}")
        replacement(cli_interface_module, data_conf['gpon-onu1'][2], " vlan ", vlan_onu1_1[i])
        replacement(cli_interface_module, data_conf['gpon-onu1'][3], " vlan ", vlan_onu1_1[i])
    vlan_onu1_2 = [117, 118, 119, 220, 221, 222]
    for i in range(0,6):
        set_and_check_config_interface(cli_interface_module, data_conf['gpon-onu1'][:2], f"gpon-onu1/2:{i+1}")
        replacement(cli_interface_module, data_conf['gpon-onu1'][2], " vlan ", vlan_onu1_2[i])
        replacement(cli_interface_module, data_conf['gpon-onu1'][3], " vlan ", vlan_onu1_2[i])
    set_and_check_config_total(cli_interface_module, data_conf['total'])
    set_and_check_config_interface(cli_interface_module, data_conf['gpon-olt1'][1:], "gpon-olt1/1")
    set_and_check_config_interface(cli_interface_module, data_conf['gpon-olt1'][1:], "gpon-olt1/2")
    set_and_check_config_interface(cli_interface_module, data_conf['ge1/1'], "ge1/1")
    set_and_check_config_interface(cli_interface_module, data_conf['ge1/2'], "ge1/2")



def test_Service(cli_interface_module):
    Service_1(cli_interface_module, config_Service_1)
    # Service_2(cli_interface_module, config_Service_2)
    



       