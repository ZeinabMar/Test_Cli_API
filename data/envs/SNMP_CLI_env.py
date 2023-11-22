from pytest_sina_framework import SecretText
DICT__SHELF = {
    'type': "Shelf_OLT",
    'node_id': None,
    'shelf_id': "int",#1
    'slot_id': "int",#1
    'index': "int",
    'snmp_ip': "192.168.9.130",
    'snmp_community': "sina_private",
    'snmp_version': "2",
    'ssh_ip':"192.168.9.130",
    'ssh_password': SecretText("sina"),
    'ssh_username': "root",
    'cli_exec_username': "admin",
    "cli_exec_password": SecretText("admin"),
    "cli_exec_password": SecretText("admin"),
    'cli_enable_password': SecretText(""),
    'cli_config_password': SecretText(""),
    'cli_debug_password': SecretText("")
}

DICT__ENV = {
    'shelf_olt': DICT__SHELF
}

