config_Senario_1 = {'total':["bridge 1 protocol ieee"],
                    'gponolt1':
                    ["max-frame 1850",
                    "flowctrl tx",
                    "description",
                    "switchport",
                    "bridge-group 1 spanning-tree enable"
                    ],
                    'gponolt2':[
                    "max-frame 1950", 
                    "flowctrl rx",
                    "description",
                    "switchport",
                    "bridge-group 1 spanning-tree disable"],
                    'gponolt3':
                    ["max-frame 2550", 
                    "switchport", 
                    "bridge-group 1 spanning-tree enable stp"]}

config_check_Senario_1 = {'total':["bridge 1 protocol ieee"],
                            'gponolt1':
                            ["max-frame 1850",
                            "flowctrl TX",
                            "description",
                            "switchport",
                            "bridge-group 1 spanning-tree enable"],
                            'gponolt2':[
                            "max-frame 1950", 
                            "flowctrl RX",
                            "description",
                            "switchport",
                            "bridge-group 1 spanning-tree disable"],
                            'gponolt3':
                            ["max-frame 2550", 
                            "switchport", 
                            "bridge-group 1 spanning-tree enable stp"]}

#**************************************************************************************
config_Senario_2 = {'total':["bridge 1 protocol ieee", 
                    "spanning-tree bridge 1 portfast bpdu-filter",
                    "spanning-tree bridge 1 portfast bpdu-guard"],
                    'ge1/1':
                    ["speed 1G",
                    "max-frame 1600",
                    "switchport",
                    "bridge-group 1 spanning-tree enable",
                    "spanning-tree bpdu-filter enable",
                    "spanning-tree bpdu-guard disable"
                    ],
                    'ge1/2':[
                    "speed 1G", 
                    "max-frame 1700",
                    "description",
                    "switchport",
                    "bridge-group 1 spanning-tree enable"
                    "spanning-tree bpdu-filter disable",
                    "spanning-tree bpdu-guard enable"],
                    'ge1/3':
                    ["speed 10G", 
                    "max-frame 1800", 
                    "description",
                    "switchport",
                    "bridge-group 1 spanning-tree disable",
                    "spanning-tree bpdu-filter enable",
                    "spanning-tree bpdu-guard enable",
                    "mirror both destination interface ge1/4"]}

config_check_Senario_2 = {'total':["bridge 1 protocol ieee", 
                        "spanning-tree bridge 1 portfast bpdu-filter",
                        "spanning-tree bridge 1 portfast bpdu-guard"],
                        'ge1/1':
                        ["speed 1G",
                        "max-frame 1600",
                        "switchport",
                        "bridge-group 1 spanning-tree enable",
                        "spanning-tree bpdu-filter enable",
                        "spanning-tree bpdu-guard disable"
                        ],
                        'ge1/2':[
                        "speed 10G", 
                        "max-frame 1700",
                        "description",
                        "switchport",
                        "bridge-group 1 spanning-tree enable"
                        "spanning-tree bpdu-filter disable",
                        "spanning-tree bpdu-guard enable"],
                        'ge1/3':
                        ["speed 10G", 
                        "max-frame 1800", 
                        "description",
                        "switchport",
                        "bridge-group 1 spanning-tree disable",
                        "spanning-tree bpdu-filter enable",
                        "spanning-tree bpdu-guard enable",
                        "mirror both destination interface ge1/4"]}                            
#**************************************************************************************
