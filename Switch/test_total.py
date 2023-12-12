import time
import pytest
import logging
import paramiko
from collections import namedtuple
import pytest_check as check
from conftest import *
from config import *
# from Switch.test_Bridge_config import test_Bridge_definition
# from Switch.test_Vlan_config import test_Vlan_management
# from Switch.test_Bridge_Group_config import test_Switch_config
# from Switch.test_Uplink_port_Vlan_config import test_Uplink_Vlan
# from Switch.test_Uplink_Port_L2_configuration import test_Uplink_Port_L2_configuration
# from Switch.test_static_rout_configuration import test_Static_Rout_configuration
# from Switch.test_Port_L3_configuration import test_Port_L3_configuration
# from Switch.test_IGMP_Configuration import test_IGMP_Configuration
# from Switch.test_Qos_management import test_Qos_Management
# from Switch.test_Qos_class_definition import test_Qos_class_definition
# from Switch.test_Port_Qos_policy_configuration import test_Port_Qos_policy_configuration
from Switch.test_QinQ_regirtration_table_configuration import test_QinQ_Registraion
from Switch.test_Port_QinQ_Translation import test_Port_QinQ_Translation
from Switch.test_Bridge_Stp import test_Bridge_Stp_Configuration
from Switch.test_Port_Storm_Control import test_Port_Storm_Control_Config
from Switch.test_Port_Stp import test_Port_Stp_Configuration
from Switch.test_Bridge_Mstp_Instance import test_Bridge_Mstp_Instance_Config
from Switch.test_Port_Mirror import test_Port_Mirror_Configuration
from Switch.test_Port_Mstp_configuration import test_Port_Mstp_Config
from Switch.test_Qos_policy_configuration_new_featue import test_Qos_Policy_configuration
from Switch.test_Port_QinQ_Registration import test_Port_QinQ_Registeration_config
# from Switch.test_Lacp_management import test_Lacp_management
# from Switch.test_Lacp_Interface import test_Lacp_Interface

pytestmark = [pytest.mark.env_name("SNMP_CLI_env"), pytest.mark.cli_dev(Test_Target)]

# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)

# def test_total(cli_interface_module):
    # test_Bridge_definition(cli_interface_module)
    # test_Vlan_management(cli_interface_module)
    # test_Switch_config(cli_interface_module)
    # test_Uplink_Vlan(cli_interface_module)
    # test_Uplink_Port_L2_configuration(cli_interface_module)
    # test_Static_Rout_configuration(cli_interface_module)
    # test_Port_L3_configuration(cli_interface_module)
    # test_IGMP_Configuration(cli_interface_module)
    # test_Qos_Management(cli_interface_module)
    # test_Qos_class_definition(cli_interface_module)
    # test_Port_Qos_policy_configuration(cli_interface_module)
    # test_QinQ_Registraion(cli_interface_module)
    # test_Port_QinQ_Translation(cli_interface_module)
    # test_Bridge_Stp_Configuration(cli_interface_module)
    # test_Port_Storm_Control_Config(cli_interface_module)
    # test_Port_Stp_Configuration(cli_interface_module)
    # test_Bridge_Mstp_Instance_Config(cli_interface_module)
    # test_Port_Mirror_Configuration(cli_interface_module)
    # test_Port_Mstp_Config(cli_interface_module)
    # test_Qos_policy_configuration_new_featue(cli_interface_module)
    # test_Port_QinQ_Registeration_config(cli_interface_module)
    # test_Lacp_management(snmp_interface_function, data, index)
    # test_Lacp_Interface(snmp_interface_function, data)