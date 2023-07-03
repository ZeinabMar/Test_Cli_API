
def get_result(cli_interface_module, grep_config, interface = True):
    if interface:
        result = str(cli_interface_module.exec(f"show running-config interface | grep {grep_config}"))
    else:
        result = str(cli_interface_module.exec(f"show running-config | grep {grep_config}"))
    result = '\n'.join(result.split('\n')[1:-1])
    return result
