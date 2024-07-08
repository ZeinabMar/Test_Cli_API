import pytest
import logging
import paramiko
import time
from collections import namedtuple
import pytest_check as check
from config import *
from conftest import *
import socket

pytestmark = [pytest.mark.env_name("SNMP_CLI_env"), pytest.mark.cli_dev(Test_Target)]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)




# def ssh_connect(IP,username, password):
#     ssh = paramiko.SSHClient()
#     try:
#         while not(is_ssh_connected(ssh)):
#             ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#             ssh.connect(IP, username=username, password=password, port=22, look_for_keys=False, timeout=10)
#             if not(ssh):
#                 with open(f'report.txt', 'a') as f:
#                     f.write(f'\n  ****************************   SSH Cant CONNECTED  ********************************   \n\n ')
#             else:
#                 return ssh 
                    
#     except paramiko.AuthenticationException:
#         logger.exception("SSH Connect Authentication Failed")
#         pass
#     except socket.timeout:
#         logger.exception("SSH Connect Timeout")
#         pass
#     except paramiko.ssh_exception.NoValidConnectionsError:
#         pass
#     except paramiko.ssh_exception.SSHException:
#         pass

    # if is_ssh_connected(ssh) == False:
    #     raise(paramiko.SSHException)
    # else:
    #     return ssh 


def is_ssh_connected(ssh):
        if ssh.get_transport():
            transport = ssh.get_transport()
            if transport.is_authenticated():
                return True
        return False

def ssh_connect(IP,username, password):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(IP, username=username, password=password, port=22, look_for_keys=False, timeout=10)
    except paramiko.AuthenticationException:
        logger.exception("SSH Connect Authentication Failed")
        pass
    except socket.timeout:
        logger.exception("SSH Connect Timeout")
        pass
    except paramiko.ssh_exception.NoValidConnectionsError:
        pass 
    except EOFError:
        pass  
    except paramiko.ssh_exception.AuthenticationException:
        pass 

    if is_ssh_connected(ssh) == False:
        logger.exception(paramiko.SSHException)
        pass
    else:
        return ssh 
    

def test_run_fpga(cli_interface_module):
    while True:
        ssh_client_olt = ssh_connect("192.168.9.127","root","sbkt4v")
        logger.info(f"ssshhh  {ssh_client_olt}")
        if ssh_client_olt != None and ssh_client_olt != False :
            if cli_interface_module.is_ssh_connected():
                # cli_interface_module.exec("su admin")    
                cli_interface_module.exec("en")    
                detail_result = cli_interface_module.exec("show version")    
                detail_result = '\n'.join(detail_result.split('\n')[1:-1])  
                result_expected = "Serial Num           : 2b00001bb11e2501"
                if len(detail_result)!=0:
                    if (detail_result.find(result_expected)!=-1):
                        with open(f'report3.txt', 'a') as f:
                            f.write(f'\n  **************************** \n   {detail_result} :  ********************************   \n\n   \n  ****************************   Serial Number is  Correct:  ********************************   \n\n ')
                    else:        
                        with open(f'report3.txt', 'a') as f:
                            f.write(f'\n  **************************** \n   {detail_result} :  ********************************   \n\n  \n  ****************************   Serial Number is  INCORRECT:  ********************************   \n\n ')        
                    cli_interface_module.exec("reboot cold")
                    cli_interface_module.exec("y")
                    cli_interface_module.exec("n")
                    cli_interface_module.close()
                    ssh_client_olt.close()
                    time.sleep(60)
            else:
                cli_interface_module.__init__(ip = "192.168.9.127",username="admin",password="admin",)
                logger.info("please Wait")
                time.sleep(1)
            
            



        



    