import time
import pytest
import logging
from clilib import CliInterface
import paramiko
from collections import namedtuple
import pytest_check as check
from conftest import *
from config import *
from PON.test_MulticasState import test_Muticast_Configuration
from PON.test_IPTV_Configuration import test_IPTV_Configuration




pytestmark = [pytest.mark.env_name("SNMP_CLI_env"), pytest.mark.snmp_dev("shelf_olt")]

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def test_total(cli_interface_module):
    test_Muticast_Configuration(cli_interface_module)
    test_IPTV_Configuration(cli_interface_module)