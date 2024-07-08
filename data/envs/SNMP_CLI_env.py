from pytest_sina_framework import SecretText
DICT__SHELF = {
    'type': "Shelf_OLT",
    'node_id': None,
    'shelf_id': "int",#1
    'slot_id': "int",#1
    'index': "int",
    'snmp_ip': "192.168.9.127",
    'snmp_community': "sina_private",
    'snmp_version': "2",
    'ssh_ip': "192.168.9.127",
    'ssh_password': SecretText("admin"),
    'ssh_username': "admin",
    'cli_exec_username': "admin",
    "cli_exec_password": SecretText("admin"),
    'cli_enable_password': SecretText(""),
    'cli_config_password': SecretText(""),
    'cli_debug_password': SecretText("")
}

DICT__SERVER = {
    'type': "server",
    'ssh_ip': "192.168.9.127",
    'ssh_password': SecretText("sbkt4v"),
    'ssh_username': "root",
    'ssh_port': "22"
}
DICT__ENV = {
    'ssh_connect' : DICT__SERVER,
    'shelf_olt': DICT__SHELF
}

