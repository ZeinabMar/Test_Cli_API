import pytest
import logging
import paramiko
from clilib import CliInterface
import time
from collections import namedtuple
import pytest_check as check
from schema import Use
from config_service import *
import time



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

def replacement(cli_interface_module, config=None, parameter=None, value_param=None, total=False, replacement_checking=None ):
    for i in range(0,len(value_param)):
        config = config.replace(parameter[i], f"{value_param[i]}")
    cli_interface_module.exec(config)
    logger.info(f"pass interface set step with {config}")
    if total == True:
        if replacement_checking!=None:
            result = str(cli_interface_module.exec(f"show running-config | grep {replacement_checking}"))
            config = replacement_checking
        else:       
            result = str(cli_interface_module.exec(f"show running-config | grep {config}"))
    else:
        if replacement_checking!=None :
            result = str(cli_interface_module.exec(f"show running-config interface| grep {replacement_checking}"))
            config = replacement_checking
        else:   
            result = str(cli_interface_module.exec(f"show running-config interface | grep {config}"))
    result = '\n'.join(result.split('\n')[1:-1])
    logger.info(f"resuuu {result}")
    assert (result.find(config)!=-1),f"NOT EXIST THIS CONFIG {config} IN INTERFACE AFTER SET"
    # check.is_in(config, result, msg= f"NOT EXIST THIS CONFIG {config} IN INTERFACE AFTER SET")

def set_reg(cli_interface_module, reg=reg):
    string_check_1 = f"registration table {reg.name} bridge 1 cvlan "
    string_check_2 = " svlan"
    for i in range(0,len(reg.cvlan)):
        string_check_1 = string_check_1+f"{reg.cvlan[i]}, "
        string_check_2 = string_check_2+f" {reg.svlan[i]},"

    string_config_1 = f"registration table {reg.name} bridge 1 cvlan "
    string_config_2 = " svlan "    
    for i in range(0,len(reg.cvlan)):    
        string_config_1 = string_config_1+f"{reg.cvlan[i]},"
        string_config_2 = string_config_2+f"{reg.svlan[i]},"  

    string_check= string_check_1+string_check_2    
    string_config= string_config_1+string_config_2    
    logger.info(f"checking: {string_check}")  
    logger.info(f"conf : {string_config}")  

    cli_interface_module.exec(string_config)
    result = str(cli_interface_module.exec(f"show running-config | grep registration"))
    result = '\n'.join(result.split('\n')[1:-1])
    assert (result.find(string_check)!=-1),f"NOT EXIST THIS CONFIG reg  AFTER SET "

def check(cli_interface_module,grep, total=True):
    if total==True:
        result = str(cli_interface_module.exec(f"show running-config | grep {grep}"))
    else:
        result = str(cli_interface_module.exec(f"show running-config interface | grep {grep}"))
    result = '\n'.join(result.split('\n')[1:-1])
    assert (result.find(grep)!=-1),f"NOT EXIST THIS CONFIG {grep}  AFTER SET "

def set_trans(cli_interface_module, trans=trans):
    string_check_1 = f"switchport QinQ trunk translation svlan-src "
    string_check_2 = " svlan-des"
    for i in range(0,len(trans.svlansrc)):
        string_check_1 = string_check_1+f"{trans.svlansrc[i]}, "
        string_check_2 = string_check_2+f" {trans.svlandes[i]},"

    string_config_1 = f"switchport QinQ trunk translation svlan-src "
    string_config_2 = " svlan-des "    
    for i in range(0,len(trans.svlansrc)):    
        string_config_1 = string_config_1+f"{trans.svlansrc[i]},"
        string_config_2 = string_config_2+f"{trans.svlandes[i]},"  

    string_check= string_check_1+string_check_2    
    string_config= string_config_1+string_config_2    
    logger.info(f"checkingg : {string_check}")  
    logger.info(f"confff : {string_config}")  

    cli_interface_module.exec(string_config)
    result = str(cli_interface_module.exec(f"show running-config | grep translation"))
    result = '\n'.join(result.split('\n')[1:-1])
    assert (result.find(string_check)!=-1),f"NOT EXIST THIS CONFIG reg  AFTER SET "

def set_and_check_config_interface(cli_interface_module,config_array, index_port, replacement_checking=None):
    command = "interface "+index_port
    cli_interface_module.exec(command)
    for i in range(0,len(config_array)):
        cli_interface_module.exec(f"{config_array[i]}")
        logger.info(f"pass interface set step with {config_array[i]}")

        if replacement_checking!=None:
            result = str(cli_interface_module.exec(f"show running-config interface| grep {replacement_checking}"))
            config_array[i] = replacement_checking
        else:       
            result = str(cli_interface_module.exec(f"show running-config interface| grep {config_array[i]}"))
        logger.info(f"resullt {result}")
        result = '\n'.join(result.split('\n')[1:-1])
        assert (result.find(config_array[i])!=-1),f"NOT EXIST THIS CONFIG {config_array[i]} IN INTERFACE AFTER SET {index_port}"
        # check.is_in(config_array[i], result, msg= f"NOT EXIST THIS CONFIG {config_array[i]} IN INTERFACE AFTER SET {index_port}")

def set_and_check_config_total(cli_interface_module,config_array, gpon= False, replacement_checking=None):
    if gpon :
        if config_array.fixed != 0 :
            cli_interface_module.exec(f"profile bandwidth {config_array.name} fixed {config_array.fixed}")
        else:   
            cli_interface_module.exec(f"profile bandwidth {config_array.name} maximum {config_array.maximum}")
        logger.info(f"pass total set step with gpon profile")
        result = str(cli_interface_module.exec(f"show running-config | grep profile"))
        result = '\n'.join(result.split('\n')[1:-1])
        assert (result.find(f"profile bandwidth {config_array.name} fixed {config_array.fixed} assured {config_array.assured} maximum {config_array.maximum}")!=-1),f"NOT EXIST THIS CONFIG gpon profile bandwidth {config_array.name} IN INTERFACE AFTER SET"
    else:    
        for i in range(0,len(config_array)):
            cli_interface_module.exec(f"{config_array[i]}")
            logger.info(f"pass total set step with {config_array[i]}")
            if replacement_checking!=None:
                result = str(cli_interface_module.exec(f"show running-config | grep {replacement_checking}"))
                config_array[i] = replacement_checking
            else:       
                result = str(cli_interface_module.exec(f"show running-config | grep {config_array[i]}"))

            result = str(cli_interface_module.exec(f"show running-config | grep {config_array[i]}"))
            result = '\n'.join(result.split('\n')[1:-1])
            assert (result.find(config_array[i])!=-1),f"NOT EXIST THIS CONFIG {config_array[i]} IN INTERFACE AFTER SET"
            # check.is_in(config_array[i], result, msg= f"not exist this config {config_array[i]} in interface total config")

def Service_1(cli_interface_module, data_conf=config_Service_1):
    cli_interface_module.change_to_config()   
    # cli_interface_module.exec("gpon")
    # set_and_check_config_total(cli_interface_module, gpon("test", 0, 250, 100000), True)
    # cli_interface_module.exec("exit")
    set_and_check_config_interface(cli_interface_module, [data_conf['gpon-olt1/1'][0]], "gpon-olt1/1")
    set_and_check_config_interface(cli_interface_module, [data_conf['gpon-olt1/2'][0]], "gpon-olt1/2")
    cli_interface_module.exec("exit")
    vlan_onu1_1 = [116, 112, 113, 114,115, 111]
    priority_1 = [3]
    for i in range(0,1):
        set_and_check_config_interface(cli_interface_module, data_conf['gpon-onu'][:2], f"gpon-onu1/1:{i+1}")
        replacement(cli_interface_module, data_conf['gpon-onu'][2], ["vlan_number"], [vlan_onu1_1[i]])
        replacement(cli_interface_module, data_conf['gpon-onu'][3], ["vlan_number", "PI"], [vlan_onu1_1[i],priority_1[i]])
    vlan_onu1_2 = [221, 220, 119, 222, 117,118]
    priority_2 = [7,6]
    for i in range(0,2):
        set_and_check_config_interface(cli_interface_module, data_conf['gpon-onu'][:2], f"gpon-onu1/2:{i+1}")
        replacement(cli_interface_module, data_conf['gpon-onu'][2], ["vlan_number"], [vlan_onu1_2[i]])
        replacement(cli_interface_module, data_conf['gpon-onu'][3], ["vlan_number", "PI"], [vlan_onu1_2[i],priority_2[i]])
    cli_interface_module.exec("exit")
    set_and_check_config_total(cli_interface_module, data_conf['total'])
    set_and_check_config_interface(cli_interface_module, data_conf['gpon-olt1/1'][1:], "gpon-olt1/1")
    set_and_check_config_interface(cli_interface_module, data_conf['gpon-olt1/2'][1:], "gpon-olt1/2")
    set_and_check_config_interface(cli_interface_module, data_conf['ge'], "ge1/2")

def Service_2(cli_interface_module, data_conf=config_Service_2):
    cli_interface_module.change_to_config()   
    # cli_interface_module.exec("gpon")
    # set_and_check_config_total(cli_interface_module, gpon("test", 0, 250, 100000), True)
    # cli_interface_module.exec("exit")
    set_and_check_config_interface(cli_interface_module, [data_conf['gpon-olt1/1'][0]], "gpon-olt1/1")
    set_and_check_config_interface(cli_interface_module, [data_conf['gpon-olt1/2'][0]], "gpon-olt1/2")
    cli_interface_module.exec("exit")
    vlan_onu1_1 = [116, 111, 112, 113, 114,115]
    priority_1 = [3]
    for i in range(0,1):
        set_and_check_config_interface(cli_interface_module, data_conf['gpon-onu'][:2], f"gpon-onu1/1:{i+1}")
        replacement(cli_interface_module, data_conf['gpon-onu'][2], ["vlan_number"], [vlan_onu1_1[i]])
        replacement(cli_interface_module, data_conf['gpon-onu'][3], ["vlan_number", "PI"], [vlan_onu1_1[i],priority_1[i]])
    vlan_onu1_2 = [221, 220, 117, 118, 119, 222]
    priority_2 = [7,6]
    for i in range(0,2):
        set_and_check_config_interface(cli_interface_module, data_conf['gpon-onu'][:2], f"gpon-onu1/2:{i+1}")
        replacement(cli_interface_module, data_conf['gpon-onu'][2], ["vlan_number"], [vlan_onu1_2[i]])
        replacement(cli_interface_module, data_conf['gpon-onu'][3], ["vlan_number", "PI"], [vlan_onu1_2[i],priority_2[i]])
    cli_interface_module.exec("exit")    
    set_and_check_config_total(cli_interface_module, data_conf['total'])
    set_and_check_config_interface(cli_interface_module, data_conf['gpon-olt1/1'][1:], "gpon-olt1/1")
    set_and_check_config_interface(cli_interface_module, data_conf['gpon-olt1/2'][1:], "gpon-olt1/2")
    set_and_check_config_interface(cli_interface_module, data_conf['ge1/1'], "ge1/1")
    set_and_check_config_interface(cli_interface_module, data_conf['ge1/2'], "ge1/2")


def Service_3(cli_interface_module, data_conf=config_Service_3):
    cli_interface_module.change_to_config()   
    cli_interface_module.exec("gpon")
    set_and_check_config_total(cli_interface_module, gpon("test", 0, 250, 100000), True)
    cli_interface_module.exec("exit")
    set_and_check_config_interface(cli_interface_module, [data_conf['gpon-olt'][0]], "gpon-olt1/2")
    cli_interface_module.exec("exit")
    vlan_onu1_1 = [221,220,116]
    priority_1 = [7,6,3]
    for i in range(0,3):
        set_and_check_config_interface(cli_interface_module, data_conf['gpon-onu'][:2], f"gpon-onu1/2:{i+1}")
        replacement(cli_interface_module, data_conf['gpon-onu'][2], ["vlan_number"], [vlan_onu1_1[i]])
        replacement(cli_interface_module, data_conf['gpon-onu'][3], ["vlan_number","PI"], [vlan_onu1_1[i],priority_1[i]])
    cli_interface_module.exec("exit")
    set_and_check_config_total(cli_interface_module, data_conf['total'][:9])
    set_reg(cli_interface_module, reg("reg1", [221,116,220],[221,116,220]))
    set_and_check_config_interface(cli_interface_module, data_conf['gpon-olt'][1:], "gpon-olt1/2")
    set_and_check_config_interface(cli_interface_module, data_conf['ge'], "ge1/2")

def Service_4(cli_interface_module, data_conf=config_Service_4):
    cli_interface_module.change_to_config()   
    cli_interface_module.exec("gpon")
    set_and_check_config_total(cli_interface_module, gpon("test", 0, 250, 100000), True)
    cli_interface_module.exec("exit")
    set_and_check_config_interface(cli_interface_module, [data_conf['gpon-olt'][0]], "gpon-olt1/1")
    cli_interface_module.exec("exit")
    vlan_onu1_1 = [115,221,116]
    priority_1 = [3,6,3]
    for i in range(0,3):
        set_and_check_config_interface(cli_interface_module, data_conf['gpon-onu'][:2], f"gpon-onu1/1:{i+1}")
        replacement(cli_interface_module, data_conf['gpon-onu'][2], ["vlan_number"], [vlan_onu1_1[i]])
        replacement(cli_interface_module, data_conf['gpon-onu'][3], ["vlan_number", "PI"], [vlan_onu1_1[i],priority_1[i]])
    cli_interface_module.exec("exit")
    set_and_check_config_total(cli_interface_module, data_conf['total'][:10])
    set_reg(cli_interface_module, reg("reg1", [115,221,116],[115,221,116]))
    set_and_check_config_interface(cli_interface_module, data_conf['gpon-olt'][1:], "gpon-olt1/1")
    set_and_check_config_interface(cli_interface_module, data_conf['ge'][:5], "ge1/1")
    set_trans(cli_interface_module, trans([113,114,112],[115,221,116]))

def Service_5(cli_interface_module, data_conf=config_Service_5):
    cli_interface_module.change_to_config()   
    # cli_interface_module.exec("gpon")
    # set_and_check_config_total(cli_interface_module, gpon("HSI", 0, 250, 100000), True)
    # cli_interface_module.exec("exit")
    # cli_interface_module.exec("gpon")
    # set_and_check_config_total(cli_interface_module, gpon("VOIP", 1000, 1250, 1500), True)
    # cli_interface_module.exec("exit")
    set_and_check_config_interface(cli_interface_module, [data_conf['gpon-olt'][0]], "gpon-olt1/1")
    cli_interface_module.exec("exit")
    set_and_check_config_interface(cli_interface_module, data_conf['gpon-onu'], f"gpon-onu1/1:1")
    cli_interface_module.exec("exit")
    set_and_check_config_total(cli_interface_module, data_conf['total'])
    set_and_check_config_interface(cli_interface_module, data_conf['gpon-olt'][1:], "gpon-olt1/1")
    set_and_check_config_interface(cli_interface_module, data_conf['ge'], "ge1/1")


def Service_6(cli_interface_module, data_conf=config_Service_6):
    cli_interface_module.change_to_config()   
    # cli_interface_module.exec("gpon")
    # set_and_check_config_total(cli_interface_module, gpon("test", 0, 250, 100000), True)
    # cli_interface_module.exec("exit")
    set_and_check_config_interface(cli_interface_module, [data_conf['gpon-olt'][0]], "gpon-olt1/1")
    cli_interface_module.exec("exit")
    set_and_check_config_interface(cli_interface_module, data_conf['gpon-onu1'], f"gpon-onu1/1:1")
    cli_interface_module.exec("exit")
    set_and_check_config_interface(cli_interface_module, data_conf['gpon-onu2'], f"gpon-onu1/1:2")
    cli_interface_module.exec("exit")
    set_and_check_config_total(cli_interface_module, data_conf['total'])
    set_and_check_config_interface(cli_interface_module, data_conf['gpon-olt'][1:], "gpon-olt1/1")
    set_and_check_config_interface(cli_interface_module, data_conf['ge'], "ge1/1")
    # set_and_check_config_interface(cli_interface_module, data_conf['ge'], "ge1/4")

def Service_8(cli_interface_module, data_conf=config_Service_8):
    cli_interface_module.change_to_config()   
    cli_interface_module.exec("gpon")
    set_and_check_config_total(cli_interface_module, gpon("test", 0, 250, 100000), True)
    vlan_onu1_1 = [221,111, 112, 113, 114, 115]
    replacement(cli_interface_module, data_conf['gpon-onu'][0], ["pro-id"], [1], True)
    set_and_check_config_total(cli_interface_module, data_conf['gpon-onu'][1:3])
    priority_1 = [7]
    for i in range(0,1):    
        replacement(cli_interface_module, data_conf['gpon-onu'][3], ["vlan_number"], [vlan_onu1_1[i]], True)
        replacement(cli_interface_module, data_conf['gpon-onu'][4], ["vlan_number", "PI"], [vlan_onu1_1[i],priority_1[i]], True, replacement_checking=f"remote service 1 gem 1 uni veip vlan-mode access pvlan {vlan_onu1_1[i]}")
    cli_interface_module.exec("exit")
    cli_interface_module.exec("gpon")
    vlan_onu1_2 = [221,220,116, 118, 119,222]
    priority_2 = [7]
    replacement(cli_interface_module, data_conf['gpon-onu'][0], ["pro-id"], [2], True)
    set_and_check_config_total(cli_interface_module, data_conf['gpon-onu'][1:3])
    for i in range(0,2):
        replacement(cli_interface_module, data_conf['gpon-onu'][3], ["vlan_number"], [vlan_onu1_2[i]], True)
        replacement(cli_interface_module, data_conf['gpon-onu'][4], ["vlan_number","PI"], [vlan_onu1_2[i],priority_2[i]], True, replacement_checking=f"remote service 1 gem 1 uni veip vlan-mode access pvlan {vlan_onu1_2[i]}")
    cli_interface_module.exec("exit")

    
    set_and_check_config_interface(cli_interface_module, [data_conf['gpon-olt1/2'][0]], "gpon-olt1/2")
    # cli_interface_module.exec("interface gpon-olt1/2")
    cli_interface_module.exec("multi-onusrv-cfg onu-srvprofile 2 onu 1-2")
    cli_interface_module.exec("interface gpon-onu1/2:1")
    check(cli_interface_module,"tcont 1 profile test",False)
    check(cli_interface_module,"gemport 1 tcont 1",False)
    check(cli_interface_module,"service-port 1 gemport 1 user-vlan 221 transparent",False)
    check(cli_interface_module,"remote service 1 gem 1 uni veip vlan-mode access pvlan 221 priority 7",False)
    cli_interface_module.exec("exit")
    cli_interface_module.exec("interface gpon-onu1/2:2")
    check(cli_interface_module,"tcont 1 profile test",False)
    check(cli_interface_module,"gemport 1 tcont 1",False)
    check(cli_interface_module,"service-port 1 gemport 1 user-vlan 220 transparent",False)
    check(cli_interface_module,"remote service 1 gem 1 uni veip vlan-mode access pvlan 220 priority 6",False)
    cli_interface_module.exec("exit")

    set_and_check_config_interface(cli_interface_module, [data_conf['gpon-olt1/1'][0]], "gpon-olt1/1")
    ##cli_interface_module.exec("interface gpon-olt1/1")
    # cli_interface_module.exec("multi-onusrv-cfg onu-srvprofile 1 onu 1-1")
    # cli_interface_module.exec("interface gpon-onu1/1:1")
    # check("tcont 1 profile test",False)
    # check("gemport 1 tcont 1",False)
    # check("service-port 1 gemport 1 user-vlan 116 transparent",False)
    # check("remote service 1 gem 1 uni veip vlan-mode access pvlan 116 priority 3",False)
    # cli_interface_module.exec("exit")

    # cli_interface_module.exec("interface gpon-onu1/1:2")
    # check("tcont 1 profile test",False)
    # check("gemport 1 tcont 1",False)
    # check("service-port 1 gemport 1 user-vlan 116 transparent",False)
    # check("remote service 1 gem 1 uni veip vlan-mode access pvlan 116 priority 3",False)
    cli_interface_module.exec("exit")
    set_and_check_config_total(cli_interface_module, data_conf['total'])
    set_and_check_config_interface(cli_interface_module, data_conf['gpon-olt1/1'][2:], "gpon-olt1/1")
    set_and_check_config_interface(cli_interface_module, data_conf['gpon-olt1/2'][2:], "gpon-olt1/2")
    set_and_check_config_interface(cli_interface_module, data_conf['ge'], "ge1/2")


def Service_9(cli_interface_module, data_conf=config_Service_9):
    cli_interface_module.change_to_config()   
    # cli_interface_module.exec("gpon")
    # set_and_check_config_total(cli_interface_module, gpon("test", 0, 250, 100000), True)
    # set_and_check_config_total(cli_interface_module, data_conf['gpon'])
    # cli_interface_module.exec("exit")
    # set_and_check_config_interface(cli_interface_module, [data_conf['gpon-olt'][0]], "gpon-olt1/1")
    # cli_interface_module.exec("exit")
    vlan_onu1_1 = [116,221,220]
    priority_1 =[3,7,6]
    for i in range(0,3):    
        set_and_check_config_interface(cli_interface_module, data_conf['gpon-onu'][:2], f"gpon-onu1/1:{i+1}")
        replacement(cli_interface_module, data_conf['gpon-onu'][2], ["vlan_number"], [vlan_onu1_1[i]])
        replacement(cli_interface_module, data_conf['gpon-onu'][3], ["vlan_number", "PI"], [vlan_onu1_1[i],priority_1[i]])
    cli_interface_module.exec("exit")
    set_and_check_config_total(cli_interface_module, data_conf['total'])
    set_and_check_config_interface(cli_interface_module, data_conf['gpon-olt'][1:], "gpon-olt1/1")
    set_and_check_config_interface(cli_interface_module, data_conf['ge'], "ge1/1")

def test_Service(cli_interface_module):
    # Service_1(cli_interface_module, config_Service_1)
    # Service_2(cli_interface_module, config_Service_2)
    # Service_3(cli_interface_module, config_Service_3)
    # Service_4(cli_interface_module, config_Service_4)
    Service_5(cli_interface_module, config_Service_5)
    # Service_6(cli_interface_module, config_Service_6)
    # Service_8(cli_interface_module, config_Service_8)
    # Service_9(cli_interface_module, config_Service_9)

    



       