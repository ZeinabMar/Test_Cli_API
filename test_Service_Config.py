import pytest
import logging
import paramiko
from clilib import CliInterface
import time
from collections import namedtuple
import pytest_check as check
from schema import Use
from config import *


pytestmark = [pytest.mark.env_name("SNMP_CLI_env"), pytest.mark.cli_dev("snmp_cli")]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def set_and_check_config_interface(cli_interface_module,config_array, index_port):
    command = "interface "+index_port
    cli_interface_module.exec(command)
    for i in range(0,len(config_array)):
        cli_interface_module.exec(f"{config_array[i]}")
        logger.info(f"pass interface set step with {config_array[i]}")
        result = str(cli_interface_module.exec(f"show running-config interface {index_port}"))
        check.is_in(config_array[i], result, msg= f"NOT EXIST THIS CONFIG {config_array[i]} IN INTERFACE AFTER SET {index_port}")

def set_and_check_config_total(cli_interface_module,config_array):
    for i in range(0,len(config_array)):
        cli_interface_module.exec(f"{config_array[i]}")
        logger.info(f"pass total set step with {config_array[i]}")
        result = str(cli_interface_module.exec(f"show running-config | grep {config_array[i]}"))
        check.is_in(config_array[i], result, msg= f"not exist this config {config_array[i]} in interface total config")

def Unconfig_function(cli_interface_module, Unconfig_array, check_array_unconfig, index_port):
    if index_port != None:
        command = "interface "+index_port
        cli_interface_module.exec(command)
    lenght = len(Unconfig_array)
    for i in range(0,lenght):
        if Unconfig_array[lenght-i-1].find("no ")!=-1:
            pass
        #     Unconfig_array[lenght-i-1].replace("no ", "")
        #     logger.info(f"CHANGE CONGIH --  -->  ++  IN   {Unconfig_array[lenght-i-1]}")
        #     cli_interface_module.exec(f"{Unconfig_array[lenght-i-1]}")
        #     if index_port != None:
        #         result = str(cli_interface_module.exec(f"show running-config interface| grep {check_array[lenght-i-1]}"))
        #     else:
        #         result = str(cli_interface_module.exec(f"show running-config | grep {check_array[lenght-i-1]}"))
        #     check.is_in(check_array[lenght-i-1], result, msg= f"cant unconfig this config {Unconfig_array[lenght-i-1]}")
        else :
            cli_interface_module.exec(f"no {Unconfig_array[lenght-i-1]}")
            if index_port != None :
                result = str(cli_interface_module.exec(f"show running-config interface| grep {index_port}"))
            else:    
                result = str(cli_interface_module.exec(f"show running-config | grep {index_port}"))
            check.is_in(check_array_unconfig[lenght-i-1], result, msg= f"cant unconfig this config no {Unconfig_array[lenght-i-1]}")


def Senario_1(cli_interface_module, data_conf=config_Senario_1, data_check=config_check_Senario_1):
    cli_interface_module.change_to_config()   
    set_and_check_config_total(cli_interface_module, data_conf['total'], data_check['total'])
    set_and_check_config_interface(cli_interface_module, data_conf['gpon-olt1/1'], data_check['gpon-olt1/1'], "gpon-olt1/1") 
    # set_and_check_config_interface(cli_interface_module, data_conf['gpon-olt1/2'], data_check['gpon-olt1/2'], "gpon-olt1/2")    
    # set_and_check_config_interface(cli_interface_module, data_conf['gpon-olt1/3'], data_check['gpon-olt1/3'], "gpon-olt1/3")  
    cli_interface_module.exec("exit")
    # Unconfig_function(cli_interface_module, data_conf['gpon-olt1/3'], data_check['gpon-olt1/3'], "gpon-olt1/3")
    # Unconfig_function(cli_interface_module, data_conf['gpon-olt1/2'], data_check['gpon-olt1/2'], "gpon-olt1/2")
    # Unconfig_function(cli_interface_module, data_conf['gpon-olt1/1'], data_check['gpon-ol
    


def Senario_2(cli_interface_module, data_conf=config_Senario_2, data_check=config_check_Senario_2):
    cli_interface_module.change_to_config()   
    set_and_check_config_total(cli_interface_module, data_conf['total'], data_check['total'])
    set_and_check_config_interface(cli_interface_module, data_conf['ge1/1'], data_check['ge1/1'], "ge1/1") 
    # set_and_check_config_interface(cli_interface_module, data_conf['ge1/2'], data_check['ge1/2'], "ge1/2")    
    # set_and_check_config_interface(cli_interface_module, data_conf['ge1/3'], data_check['ge1/3'], "ge1/3")    
    cli_interface_module.exec("exit")
    # Unconfig_function(cli_interface_module, data_conf['ge1/3'], data_check['ge1/3'], "ge1/3")
    # Unconfig_function(cli_interface_module, data_conf['ge1/2'], data_check['ge1/2'], "ge1/2")
    Unconfig_function(cli_interface_module, data_conf['ge1/1'], data_check['ge1/1'], "ge1/1")
    Unconfig_function(cli_interface_module, data_conf['total'], data_check['total'], None)


def Senario_3(cli_interface_module, data_conf=config_Senario_3, data_check=config_Senario_3):
    cli_interface_module.change_to_config()   
    set_and_check_config_total(cli_interface_module, data_conf['total'], data_check['total'])
    set_and_check_config_interface(cli_interface_module, data_conf['ge1/1'], data_check['ge1/1'], "ge1/1") 
    set_and_check_config_interface(cli_interface_module, data_conf['ge1/2'], data_check['ge1/2'], "ge1/2")    
    set_and_check_config_interface(cli_interface_module, data_conf['ge1/3'], data_check['ge1/3'], "ge1/3")    
    cli_interface_module.exec("exit")
    Unconfig_function(cli_interface_module, data_conf['ge1/3'], "ge1/3")
    Unconfig_function(cli_interface_module, data_conf['ge1/2'], "ge1/2")
    Unconfig_function(cli_interface_module, data_conf['ge1/1'], "ge1/1")
    Unconfig_function(cli_interface_module, data_conf['total'], None)
      

# @pytest.mark.parametrize('data', BRIDGE_DATA)
def test_Senario(cli_interface_module):
    Senario_1(cli_interface_module, config_Senario_1, config_check_Senario_1)
    # Senario_2(cli_interface_module, config_Senario_2, config_check_Senario_2)
    # Senario_3(cli_interface_module, config_Senario_3, config_Senario_3)

