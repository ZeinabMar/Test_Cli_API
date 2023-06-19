
def get_result(cli_interface_module, grep_config, interface = True):
    if interface:
        result = str(cli_interface_module.exec(f"show running-config interface | grep {grep_config}"))
    else:
        result = str(cli_interface_module.exec(f"show running-config | grep {grep_config}"))
    result = '\n'.join(result.split('\n')[1:-1])
    return result




    # cli_interface_module.exec("interface ge1/1") 
    # cli_interface_module.exec("switchport mode access") 
    # result = cli_interface_module.exec("switchport access tag 10") 
    # result = '\n'.join(result.split('\n')[1:-1])
    # logger.info(f"result {result}")