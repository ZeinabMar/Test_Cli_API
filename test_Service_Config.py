import pytest
import logging
import paramiko
from clilib import CliInterface
import time
from collections import namedtuple
import pytest_check as check
from schema import Use

Test_Target = 'PS6x_card'

pytestmark = [pytest.mark.env_name("NP_env"), pytest.mark.cli_dev(Test_Target)]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

config_Senario_1 = {'total':["bridge 1 protocol ieee"],
                    'gponolt1':
                    ["max-frame 1850",
                    "flowctrl tx",
                    "description",
                    "switchport",
                    "bridge-group 1 spanning-tree enable"],
                    'gponolt2':[
                    "max-frame 1950", 
                    "flowctrl rx",
                    "description",
                    "switchport",
                    "bridge-group 1 spanning-tree disable"],
                    'gponolt3':
                    ["max-frame 2550", 
                    "switchport", 
                    "bridge-group 1 spanning-tree enable stp"]}

config_check_Senario_1 = {'total':["bridge 1 protocol ieee"],
                            'gponolt1':
                            ["max-frame 1850",
                            "flowctrl TX",
                            "description",
                            "switchport",
                            "bridge-group 1 spanning-tree enable"],
                            'gponolt2':[
                            "max-frame 1950", 
                            "flowctrl RX",
                            "description",
                            "switchport",
                            "bridge-group 1 spanning-tree disable"],
                            'gponolt3':
                            ["max-frame 2550", 
                            "switchport", 
                            "bridge-group 1 spanning-tree enable stp"]}

def set_and_check_config_interface(cli_interface_module,config_array, check_array, index_port):

    command = "interface "+index_port
    cli_interface_module.exec(command)
    for conf in config_array:
        cli_interface_module.exec(f"{conf}")
    cli_interface_module.exec("show running-config interface")
    result = str(cli_interface_module.exec("A")) 
    for i in range(0,len(check_array)):
        check.is_in(check_array[i], result, msg= f"NOT EXIST THIS CONFIG {check_array[i]} IN INTERFACE {index_port}")

def set_and_check_config_total(cli_interface_module,config_array, check_array):
    for conf in config_array:
        cli_interface_module.exec(f"{conf}")
    cli_interface_module.exec("show running-config")
    result = str(cli_interface_module.exec("A")) 
    for i in range(0,len(check_array)):
        check.is_in(check_array[i], result, msg= f"not exist this config {check_array[i]} in interface total config")

def Senario_1(cli_interface_module, data_conf=config_Senario_1, data_check=config_check_Senario_1):

    cli_interface_module.change_to_config()   
    set_and_check_config_total(cli_interface_module, data_conf['total'], data_check['total'])
    logger.info(f"dic {data_conf['gponolt1']}")
    set_and_check_config_interface(cli_interface_module, data_conf['gponolt1'], data_check['gponolt1'], "gpon-olt1/1") 
    # set_and_check_config_interface(cli_interface_module, data_conf['gponolt2'], data_check['gponolt2'], "gpon-olt1/2")    
    # set_and_check_config_interface(cli_interface_module, data_conf['gponolt3'], data_check['gponolt3'], "gpon-olt1/3")       


# @pytest.mark.parametrize('data', BRIDGE_DATA)
def test_Senario(cli_interface_module):
    Senario_1(cli_interface_module, config_Senario_1, config_check_Senario_1)