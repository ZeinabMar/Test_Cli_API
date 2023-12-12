import pytest
import logging
import paramiko
from collections import namedtuple
import pytest_check as check
from config import *
from conftest import *

pytestmark = [pytest.mark.env_name("SNMP_CLI_env"), pytest.mark.cli_dev(Test_Target)]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Port_Mirror = namedtuple('Port_Mirror', ['Index', 'config', "result_find", "result_error", 'result_not_find', 'grep'])
Port_Mirror.__new__.__defaults__ = (None, "", [], [], [], "")

Port_Mirror_Config_First_Port = [
  Port_Mirror(1, f"mirror both destination interface ge1/5", result_error=["Error code: -1625"], grep="mirror"),
  Port_Mirror(2, f"mirror both destination interface ge1/4", result_find=[f"mirror both destination interface ge1/4"], grep="mirror"),
  Port_Mirror(3, f"mirror ingress destination interface ge1/4", result_error=["Error code: -1625"], grep="mirror"),
  Port_Mirror(4, f"mirror egress destination interface ge1/4", result_error=["Error code: -1625"], grep="mirror"),
  Port_Mirror(5, f"mirror both destination interface ge1/6", result_find=[f"mirror both destination interface ge1/6"], grep="mirror"),
  Port_Mirror(6, f"no mirror both", result_not_find=["mirror both"], grep="mirror"),
  Port_Mirror(7, f"mirror egress destination interface ge1/6", result_find=[f"mirror egress destination interface ge1/6"], grep="mirror"),
  Port_Mirror(8, f"mirror both destination interface ge1/6", result_error=["Error code: -1625"], grep="mirror"),
  Port_Mirror(9, f"mirror ingress destination interface ge1/6", result_find=[f"mirror egress destination interface ge1/6", f"mirror ingress destination interface ge1/6"], grep="mirror"),
  Port_Mirror(10, f"mirror ingress destination interface ge1/4", result_find=[f"mirror egress destination interface ge1/6", f"mirror ingress destination interface ge1/4"], grep="mirror"),
  Port_Mirror(11, f"mirror both destination interface ge1/6", result_error=["Error code: -1625"], grep="mirror"),
  Port_Mirror(12, f"mirror egress destination interface ge1/4", result_find=[f"mirror egress destination interface ge1/4", f"mirror ingress destination interface ge1/4"], grep="mirror"),
] 

Port_Mirror_Config_Second_Port = [
 Port_Mirror(1, f"mirror both destination interface ge1/6", result_error=["Error code: -1625"], grep="mirror"),
 Port_Mirror(2, f"mirror both destination interface ge1/4", result_find=[f"mirror both destination interface ge1/4"], grep="mirror"),
 Port_Mirror(3, f"mirror ingress destination interface ge1/4", result_error=["Error code: -1625"], grep="mirror"),
 Port_Mirror(4, f"mirror egress destination interface ge1/4", result_error=["Error code: -1625"], grep="mirror"),
 Port_Mirror(5, f"mirror both destination interface ge1/5", result_find=[f"mirror both destination interface ge1/5"], grep="mirror"),
 Port_Mirror(6, f"no mirror both", result_not_find=["mirror both"], grep="mirror"),
 Port_Mirror(7, f"mirror egress destination interface ge1/5", result_find=[f"mirror egress destination interface ge1/5"], grep="mirror"),
 Port_Mirror(8, f"mirror both destination interface ge1/5", result_error=["Error code: -1625"], grep="mirror"),
 Port_Mirror(9, f"mirror ingress destination interface ge1/5", result_find=[f"mirror egress destination interface ge1/5", f"mirror ingress destination interface ge1/5"],  grep="mirror"),
 Port_Mirror(10, f"mirror ingress destination interface ge1/4", result_find=[f"mirror egress destination interface ge1/5", f"mirror ingress destination interface ge1/4"],grep="mirror"),
 Port_Mirror(11, f"mirror both destination interface ge1/5", result_error=["Error code: -1625"], grep="mirror"),
 Port_Mirror(12, f"mirror egress destination interface ge1/4", result_find=[f"mirror egress destination interface ge1/4", f"mirror ingress destination interface ge1/4"], grep="mirror"),
]


Port_Mirror_Config_Default = [
  Port_Mirror(1, "no mirror both", result_not_find=["mirror both"], grep="mirror"),
  Port_Mirror(1, "no mirror ingree", result_not_find=["mirror ingree"], grep="mirror"),
  Port_Mirror(1, "no mirror egress", result_not_find=["mirror egress"], grep="mirror"),
]

def Port_Mirror_Configuration(cli_interface_module, data=[], method="SET"):  
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

 
def test_Port_Mirror_Configuration(cli_interface_module):
    cli_interface_module.change_to_config() 
    for port in range(5,6):
        for i in range(len(Port_Mirror_Config_Second_Port)):
            if 1 <= port <=8 :
                cli_interface_module.exec(f"interface ge1/{port}") 
                Port_Mirror_Configuration(cli_interface_module, Port_Mirror_Config_First_Port[i], "SET")
                cli_interface_module.exec(f"interface ge1/{port+1}") 
                Port_Mirror_Configuration(cli_interface_module, Port_Mirror_Config_Second_Port[i], "SET")

            else:    
                cli_interface_module.exec(f"interface gpon-olt1/{port-8}") 
                Port_Mirror_Configuration(cli_interface_module, Port_Mirror_Config_First_Port[i], "SET")
                cli_interface_module.exec(f"interface gpon-olt1/{port+1-8}") 
                Port_Mirror_Configuration(cli_interface_module, Port_Mirror_Config_Second_Port[i], "SET")
        cli_interface_module.exec("exit") 
        if 1 <= port <=8 :
                cli_interface_module.exec(f"interface ge1/{port}") 
                for mirror in Port_Mirror_Config_Default:
                    Port_Mirror_Configuration(cli_interface_module, mirror, "DEFAULT")
                cli_interface_module.exec(f"interface ge1/{port+1}") 
                for mirror in Port_Mirror_Config_Default:
                    Port_Mirror_Configuration(cli_interface_module, mirror, "DEFAULT")

        else:    
            cli_interface_module.exec(f"interface gpon-olt1/{port-8}") 
            for mirror in Port_Mirror_Config_Default:
                Port_Mirror_Configuration(cli_interface_module, mirror, "DEFAULT")
            cli_interface_module.exec(f"interface gpon-olt1/{port+1-8}") 
            for mirror in Port_Mirror_Config_Default:
                    Port_Mirror_Configuration(cli_interface_module, mirror, "DEFAULT")

# def Port_Mirror_Configuration(cli_interface_module, data=[], method="SET", gpon=None):  
#     logger.info(f'PORT MIRROR TEST DATA ------- > {data.Index} IN METHODE {method}')  
#     result_find = data.result_find
#     result_error = data.result_error
#     result_not_find = data.result_not_find
#     grep = data.grep
#     port = data.port
#     step = data.step
#     if port <= 6 :
#         detail_result = cli_interface_module.exec(data.config+gpon+f"{port+step}") 
#     else: 
#         detail_result = cli_interface_module.exec(data.config+gpon+f"{port-step}") 
   
#     detail_result = '\n'.join(detail_result.split('\n')[1:-1])  
#     if len(result_find) != 0:
#         for f in result_find:
#             result = get_result(cli_interface_module, f"{grep}")
#             if port <= 6:
#                 assert (result.find(f+gpon+f"{port+step}")!=-1),f"NOT EXIST {f}"+gpon+f"{port+step} in config"
#             else:
#                 assert (result.find(f+gpon+f"{port-step}")!=-1),f"NOT EXIST {f}"+gpon+f"{port-step} in config"
#     if len(result_error) != 0:
#         for error in result_error:
#             assert (detail_result.find(error)!=-1),f"APPLY ERROR DATA"
#     if len(result_not_find) != 0:
#         for nf in result_not_find:
#             result = get_result(cli_interface_module, f"{grep}")
#             assert (result.find(nf)==-1),f"FIND {data.config} IN CONFIG OF SYSTEM AND NOT TO BE CLEARED"


# def test_Port_Mirror_Configuration(cli_interface_module):
#     cli_interface_module.change_to_config() 
#     for port in range(20,21):
#         for i in range(len(Port_Mirror_Config_Second_Port)):
#             if 1 <= port <=8 :
#                 cli_interface_module.exec(f"interface ge1/{port}") 
#                 Port_Mirror_Configuration(cli_interface_module, Port_Mirror_Config_First_Port[i]._replace(port=port), "SET", " ge1/")
#                 cli_interface_module.exec(f"interface ge1/{port+1}") 
#                 Port_Mirror_Configuration(cli_interface_module, Port_Mirror_Config_Second_Port[i]._replace(port=port), "SET", " ge1/")
#             else:    
#                 cli_interface_module.exec(f"interface gpon-olt1/{port-8}") 
#                 Port_Mirror_Configuration(cli_interface_module, Port_Mirror_Config_First_Port[i]._replace(port=port-8), "SET", " gpon-olt1/")
#                 cli_interface_module.exec(f"interface gpon-olt1/{port+1-8}") 
#                 Port_Mirror_Configuration(cli_interface_module, Port_Mirror_Config_Second_Port[i]._replace(port=port+1-8), "SET", " gpon-olt1/")
#         cli_interface_module.exec("exit") 

        # if 1 <= port <=8 :
        #     cli_interface_module.exec(f"interface ge1/{port}") 
        #     for port_mirror in Port_Mirror_Config_Default:
        #         Port_Storm_Control_Config(cli_interface_module, port_mirror, "DEFAULT")  
        #     if port<=6:      
        #         cli_interface_module.exec(f"interface ge1/{port+1}") 
        #     else:    
        #         cli_interface_module.exec(f"interface ge1/{port-1}") 
        #     for port_mirror in Port_Mirror_Config_Default:
        #         Port_Storm_Control_Config(cli_interface_module, port_mirror, "DEFAULT")    
        # else:    
        #     cli_interface_module.exec(f"interface gpon-olt1/{port-8}") 
        #     for port_mirror in Port_Mirror_Config_Default:
        #         Port_Storm_Control_Config(cli_interface_module, port_mirror, "DEFAULT")   
        #     if port-8<=6:      
        #         cli_interface_module.exec(f"interface interface gpon-olt1/{port-8+1}") 
        #     else:    
        #         cli_interface_module.exec(f"interface interface gpon-olt1/{port-8-1}") 
        #     for port_mirror in Port_Mirror_Config_Default:
        #         Port_Storm_Control_Config(cli_interface_module, port_mirror, "DEFAULT")       





