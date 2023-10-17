import pytest
import logging
import paramiko
from clilib import CliInterface
import time
from collections import namedtuple
import pytest_check as check
from config import *
from conftest import *
from conftest import *
from Switch.test_Bridge_config import Bridge_definition
from Switch.test_Vlan_config import vlan_management
import colorlog




pytestmark = [pytest.mark.env_name("SNMP_CLI_env"), pytest.mark.cli_dev(Test_Target)]

handler = colorlog.StreamHandler()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.addHandler(handler)

QinQ_Registration = namedtuple('QinQ_Registration', ['Index', 'config', "result_find", "result_error", 'result_not_find', 'grep'])
QinQ_Registration.__new__.__defaults__ = (None, "", [], [], [], "")


QinQ_Registration_DATA = [
 QinQ_Registration(1, "registration table reg1 bridge 2 cvlan 15 svlan 16", result_error=["Invalid bridge ID"]),
#  QinQ_Registration(2, "registration table reg1 bridge 1 cvlan 15 svlan 16", result_error=["Error code: -1633"], result_not_find=[" registration table reg1 bridge 1 cvlan  svlan"], grep="registration"),
#  QinQ_Registration(3, "registration table reg1 bridge 1 cvlan 10 svlan 11", result_error=["Error code: -1633"], result_not_find=[" registration table reg1 bridge 1 cvlan  svlan"], grep="registration"),
 QinQ_Registration(4, "registration table reg1 bridge 1 cvlan 10-12 svlan 14-16", result_find=[" registration table reg1 bridge 1 cvlan 10,  svlan 14,"], grep="registration"),
 QinQ_Registration(5, "registration table reg2 bridge 1 cvlan 12 svlan 16", result_find=[" registration table reg2 bridge 1 cvlan 12,  svlan 16,"], grep="registration"),
 QinQ_Registration(6, "registration table reg2 bridge 1 cvlan 10 svlan 14", result_find=[" registration table reg2 bridge 1 cvlan 12, 10,  svlan 16, 14,"], grep="registration"),
 QinQ_Registration(7, "no registration table reg2 bridge 1 cvlan 10", result_find=[" registration table reg2 bridge 1 cvlan 12,  svlan 16,"], grep="registration"),
 QinQ_Registration(8, "no registration table reg2 bridge 1 cvlan 12", result_find=[" registration table reg2 bridge 1 cvlan  svlan"], grep="registration"),  
]

QinQ_Registration_Delete = [
 QinQ_Registration(1, "no registration table reg1 bridge 1", result_not_find=[" registration table reg1"], grep="registration"),
 QinQ_Registration(2, "no registration table reg2 bridge 1", result_not_find=[" registration table reg2"], grep="registration"),
]

def QinQ_Registraion(cli_interface_module, data=QinQ_Registration(), method =None): 
    handler.setFormatter(colorlog.ColoredFormatter('%(green)s%(levelname)s:%(name)s:%(message)s'))    
    logger.info(f"    ***************QINQ REGISTRATION CONFIGURATION*************************")
    if method == "SET":
        handler.setFormatter(colorlog.ColoredFormatter('%(red)s%(levelname)s:%(name)s:%(message)s'))
        logger.info(f"   ************SET   MODE********************   ")
    else:
        logger.info(f"   ************DELETE   MODE********************   ")
    handler.setFormatter(colorlog.ColoredFormatter('%(yellow)s%(levelname)s:%(name)s:%(message)s'))    
    logger.info(f"       ************IN DATE WITH INDEX  {data.Index}  ************")

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

def test_QinQ_Registraion(cli_interface_module):
    cli_interface_module.change_to_config() 
    Bridge_definition(cli_interface_module, bridge_service_custom[0])
    for vlan_custom in Vlan_Custom:
        vlan_management(cli_interface_module, vlan_custom)
    for vlan_service in Vlan_Service:  
        vlan_management(cli_interface_module, vlan_service)

    for qinq_reg in QinQ_Registration_DATA:
        QinQ_Registraion(cli_interface_module, qinq_reg, "SET")

    for qinq_reg_del in QinQ_Registration_Delete:
        QinQ_Registraion(cli_interface_module, qinq_reg_del, "DELETE")


    for vlan_custom_del in Vlan_Custom_DELETE:  
        vlan_management(cli_interface_module, vlan_custom_del)
    for vlan_service_del in Vlan_Service_DELETE:  
        vlan_management(cli_interface_module, vlan_service_del)
    Bridge_definition(cli_interface_module, bridge_definition_DELETE)
