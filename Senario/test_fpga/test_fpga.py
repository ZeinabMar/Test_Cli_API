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
    except socket.timeout:
        logger.exception("SSH Connect Timeout")

    if is_ssh_connected(ssh) == False:
        raise(paramiko.SSHException)
    else:
        return ssh 
    

def test_run_fpga(cli_interface_module):
    while True:
        ssh_client_olt = ssh_connect("192.168.9.127","root","sbkt4v")
        logger.info(f"ssshhh  {ssh_client_olt}")
        if ssh_client_olt != None and ssh_client_olt != False :
        # cli_interface_module.change_to_config() 
                stdin1,output1,err1 = ssh_client_olt.exec_command(f"su admin", 3)
                stdin2,output2,err2 = ssh_client_olt.exec_command(f"en", 3)
                stdin3,output3,err3 = ssh_client_olt.exec_command(f"show version", 3)
                logger.info(f"outpuuut {output3.read()}")

                result_expected = "Serial Num           : 2b00001bb11e2501"
                out = []
                for line_olt in output3:
                    logger.info(f"line : {line_olt.strip()}")
                    out.append(str(line_olt.strip()))

                # if (out.find(result_expected)!=-1):
                #     with open(f'report.txt', 'a') as f:
                #         f.write(f'\n  **************************** \n   {out} :  ********************************   \n\n   \n  ****************************   Serial Number is  Correct:  ********************************   \n\n ')
                # else:        
                #     with open(f'report.txt', 'a') as f:
                #         f.write(f'\n  **************************** \n   {out} :  ********************************   \n\n  \n  ****************************   Serial Number is  INCORRECT:  ********************************   \n\n ')        
                # stdin4,output4,err4 = ssh_client_olt.exec_command(f"reboot cold", 3)
                # stdin4,output4,err4 = ssh_client_olt.exec_command(f"y", 3)
                # stdin4,output4,err4 = ssh_client_olt.exec_command(f"n", 3)

        # else:
        #     logger.info("please Wait")
        #     time.sleep(1)
        
            



        



    