import pytest
import logging
import paramiko
from clilib import CliInterface
import time
from collections import namedtuple
import pytest_check as check
from schema import Use
from config import *

Test_Target = 'PS6x_card'

pytestmark = [pytest.mark.env_name("NP_env"), pytest.mark.cli_dev(Test_Target)]

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
        

def Senario_1(cli_interface_module, data_conf=config_Senario_1, data_check=config_check_Senario_1):
    cli_interface_module.change_to_config()   
    set_and_check_config_total(cli_interface_module, data_conf['total'], data_check['total'])
    set_and_check_config_interface(cli_interface_module, data_conf['gponolt1'], data_check['gponolt1'], "gpon-olt1/1") 
    set_and_check_config_interface(cli_interface_module, data_conf['gponolt2'], data_check['gponolt2'], "gpon-olt1/2")    
    set_and_check_config_interface(cli_interface_module, data_conf['gponolt3'], data_check['gponolt3'], "gpon-olt1/3")       

def Senario_2(cli_interface_module, data_conf=config_Senario_2, data_check=config_check_Senario_2):
    # cli_interface_module.change_to_config()   
    # set_and_check_config_total(cli_interface_module, data_conf['total'], data_check['total'])
    set_and_check_config_interface(cli_interface_module, data_conf['ge1/1'], data_check['ge1/1'], "ge1/1") 
    # set_and_check_config_interface(cli_interface_module, data_conf['ge1/2'], data_check['ge1/2'], "ge1/2")    
    # set_and_check_config_interface(cli_interface_module, data_conf['ge1/3'], data_check['ge1/3'], "ge1/3")       

# @pytest.mark.parametrize('data', BRIDGE_DATA)
def test_Senario(cli_interface_module):
    # Senario_1(cli_interface_module, config_Senario_1, config_check_Senario_1)
    Senario_2(cli_interface_module, config_Senario_2, config_check_Senario_2)