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


def set_and_check_config_interface(cli_interface_module,config_array, check_array, index_port):
    command = "interface "+index_port
    cli_interface_module.exec(command)
    for i in range(0,len(config_array)):
        cli_interface_module.exec(f"{config_array[i]}")
        result = str(cli_interface_module.exec(f"show running-config interface | grep {check_array[i]}"))
        check.is_in(check_array[i], result, msg= f"NOT EXIST THIS CONFIG {check_array[i]} IN INTERFACE {index_port}")

def set_and_check_config_total(cli_interface_module,config_array, check_array):
    for i in range(0,len(config_array)):
        cli_interface_module.exec(f"{config_array[i]}")
        result = str(cli_interface_module.exec(f"show running-config | grep {config_array[i]}"))
        check.is_in(check_array[i], result, msg= f"not exist this config {check_array[i]} in interface total config")

def Unconfig_interface(cli_interface_module,Unconfig_array, index_port):
    command = "interface "+index_port
    cli_interface_module.exec(command)
    for i in range(0,len(Unconfig_array)):
        cli_interface_module.exec(f"{Unconfig_array[i]}")

def Unconfig_total(cli_interface_module,Unconfig_array):
    lenght = len(Unconfig_array)
    for i in range(0,lenght):
        if Unconfig_array[lenght-i].find("no ")!=-1 or Unconfig_array[lenght-i].find("disable")!=-1:
            Unconfig_array[lenght-i].replace("no ", "")
            Unconfig_array[lenght-i].replace("disable", "enable")
            cli_interface_module.exec(f"{Unconfig_array[lenght-i]}")
        else :
            cli_interface_module.exec(f"no {Unconfig_array[lenght-i]}")


def Senario_1(cli_interface_module, data_conf=config_Senario_1, data_check=config_check_Senario_1, data_unconfig=Unconfig_Senario_1):
    cli_interface_module.change_to_config()   
    set_and_check_config_total(cli_interface_module, data_conf['total'], data_check['total'])
    set_and_check_config_interface(cli_interface_module, data_conf['gponolt1'], data_check['gponolt1'], "gpon-olt1/1") 
    set_and_check_config_interface(cli_interface_module, data_conf['gponolt2'], data_check['gponolt2'], "gpon-olt1/2")    
    set_and_check_config_interface(cli_interface_module, data_conf['gponolt3'], data_check['gponolt3'], "gpon-olt1/3")  
    cli_interface_module.exec("exit")
    Unconfig_interface(cli_interface_module, data_conf['gponolt3'], "gpon-olt1/3")
    Unconfig_interface(cli_interface_module, data_conf['gponolt2'], "gpon-olt1/2")
    Unconfig_interface(cli_interface_module, data_conf['gponolt1'], "gpon-olt1/1")
    Unconfig_total(cli_interface_module, data_unconfig['total'])


def Senario_2(cli_interface_module, data_conf=config_Senario_2, data_check=config_check_Senario_2):
    cli_interface_module.change_to_config()   
    set_and_check_config_total(cli_interface_module, data_conf['total'], data_check['total'])
    set_and_check_config_interface(cli_interface_module, data_conf['ge1/1'], data_check['ge1/1'], "ge1/1") 
    set_and_check_config_interface(cli_interface_module, data_conf['ge1/2'], data_check['ge1/2'], "ge1/2")    
    set_and_check_config_interface(cli_interface_module, data_conf['ge1/3'], data_check['ge1/3'], "ge1/3")    
    cli_interface_module.exec("exit")
    Unconfig_interface(cli_interface_module, data_unconfig['ge1/3'], "ge1/3")
    Unconfig_interface(cli_interface_module, data_unconfig['ge1/2'], "ge1/2")
    Unconfig_interface(cli_interface_module, data_unconfig['ge1/1'], "ge1/1")
    Unconfig_total(cli_interface_module, data_unconfig['total'])


# def Senario_3(cli_interface_module, data_conf=config_Senario_3, data_check=config_check_Senario_3):
#     cli_interface_module.change_to_config()   
#     set_and_check_config_total(cli_interface_module, data_conf['total'], data_check['total'])
#     set_and_check_config_interface(cli_interface_module, data_conf['ge1/1'], data_check['ge1/1'], "ge1/1") 
#     set_and_check_config_interface(cli_interface_module, data_conf['ge1/2'], data_check['ge1/2'], "ge1/2")    
#     set_and_check_config_interface(cli_interface_module, data_conf['ge1/3'], data_check['ge1/3'], "ge1/3")    
#     cli_interface_module.exec("exit")
#     Unconfig_interface(cli_interface_module, data_unconfig['ge1/3'], "ge1/3")
#     Unconfig_interface(cli_interface_module, data_unconfig['ge1/2'], "ge1/2")
#     Unconfig_interface(cli_interface_module, data_unconfig['ge1/1'], "ge1/1")
#     Unconfig_total(cli_interface_module, data_unconfig['total'])
      

# @pytest.mark.parametrize('data', BRIDGE_DATA)
def test_Senario(cli_interface_module):
    Senario_1(cli_interface_module, config_Senario_1, config_check_Senario_1, Unconfig_Senario_1)
    # Senario_2(cli_interface_module, config_Senario_2, config_check_Senario_2, Unconfig_Senario_2)