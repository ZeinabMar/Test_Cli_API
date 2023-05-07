config_Senario_1 = {'total':["bridge 1 protocol ieee"],
                    'gpon-olt1/1':
                    ["max-frame 1850",
                    "flowctrl tx",
                    "description",
                    "switchport",
                    "bridge-group 1 spanning-tree enable"
                    ],
                    'gpon-olt1/2':[
                    "max-frame 1950", 
                    "flowctrl rx",
                    "description",
                    "switchport",
                    "bridge-group 1 spanning-tree disable"],
                    'gpon-olt1/3':
                    ["max-frame 2550", 
                    "switchport", 
                    "bridge-group 1 spanning-tree enable stp"]}

unconfig_Senario_1 = {'total':["no bridge 1 protocol ieee"],
                    'gpon-olt1/1':
                    ["no max-frame",
                    "no flowctrl tx",
                    "no description",
                    "no switchport",
                    "no bridge-group 1 spanning-tree enable"
                    ],
                    'gpon-olt1/2':[
                    "no max-frame 1950", 
                    "no flowctrl rx",
                    "no description",
                    "no switchport",
                    "no bridge-group 1 spanning-tree disable"],
                    'gpon-olt1/3':
                    ["no max-frame 2550", 
                    "no switchport", 
                    "no bridge-group 1 spanning-tree enable stp"]}

unconfig_check_Senario_1 = {'total':[{"empty":"bridge"}],
                            'gpon-olt1/1':
                            [{"command":"max-frame 1500"},
                            {"command":"no flowctrl"},
                            {"command":"no description"},
                            {"command":"no switchport"},
                            {"empty":"bridge-group 1 spanning-tree"}
                            ],
                            'gpon-olt1/2':[
                            "max-frame 1950", 
                            "flowctrl RX",
                            "description",
                            "switchport",
                            "bridge-group 1 spanning-tree disable"],
                            'gpon-olt1/3':
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
                        "mirror both destination ge1/4"]}                            
#**************************************************************************************
config_Senario_3 = {'total':["bridge 1 protocol ieee-vlan-bridge", 
                        "spanning-tree bridge 1 portfast bpdu-filter",
                        "spanning-tree bridge 1 portfast bpdu-guard"
                        "vlan 10 bridge 1 type customer state enable",
                        "vlan 11 bridge 1 type customer state enable",
                        "vlan 12 bridge 1 type customer state enable",
                        "vlan 13 bridge 1 type customer state enable",
                        "vlan 14 bridge 1 type customer state enable"
                        "vlan 15 bridge 1 type customer state enable"],
                    'ge1/1':
                        ["speed 1G",
                        "max-frame 1600",
                        "switchport",
                        "bridge-group 1 spanning-tree enable",
                        "switchport mode access",
                        "switchport access 10",
                        "spanning-tree bpdu-filter enable",
                        "spanning-tree bpdu-guard enable",
                        "storm-control dlf level 45",
                        "storm-control broadcast level 55"
                        ],
                    'ge1/2':[
                        "speed 1G", 
                        "max-frame 1700",
                        "description",
                        "switchport",
                        "bridge-group 1 spanning-tree enable"
                        "switchport mode trunk",
                        "switchport trunk tag 10-12",
                        "no switchport trunk tag 11",
                        "spanning-tree bpdu-filter enable",
                        "spanning-tree bpdu-guard disable",
                        "mirror ingress destination interface ge1/4"],
                    'ge1/3':
                        ["max-frame 1800", 
                        "description",
                        "switchport",
                        "bridge-group 1 spanning-tree enable",
                        "switchport mode trunk",
                        "switchport trunk tag 11,13-15",
                        "no switchport trunk tag 13",
                        "spanning-tree bpdu-filter disable",
                        "spanning-tree bpdu-guard enable",
                        "storm-control broadcast level 65",
                        "storm-control multicast level 45",
                        "no storm-control multicast"]}
#**************************************************************************
config_Senario_4 = {'total':["bridge 1 protocol rstp"],
                    'gpon-olt1/1':
                        ["max-frame 1850",
                        "flowctrl rx",
                        "switchport",
                        "bridge-group 1 spanning-tree enable",
                        "description",
                        "storm-control dlf level 38"
                        ],
                    'gpon-olt1/2':[
                        "max-frame 1950",
                        "description",
                        "switchport",
                        "bridge-group 1 spanning-tree enable"
                        "storm-control broadcast level 48",
                        "storm-control broadcast level 55"],
                    'gpon-olt1/3':
                        ["max-frame 2550", 
                        "switchport",
                        "bridge-group 1 spanning-tree enable",
                        "flowctrl tx",
                        "storm-control multicast level 45",
                        "mirror egress destination interface gpon-olt1/5",
                        "no mirror egress"]} 
config_check_Senario_4 = {'total':["bridge 1 protocol rstp"],
                    'gpon-olt1/1':
                        ["max-frame 1850",
                        "flowctrl RX",
                        "switchport",
                        "bridge-group 1 spanning-tree enable",
                        "description",
                        "storm-control dlf level 38.000000"
                        ],
                    'gpon-olt1/2':[
                        "max-frame 1950",
                        "description",
                        "switchport",
                        "bridge-group 1 spanning-tree enable"
                        "storm-control broadcast level 48.000000",
                        "storm-control broadcast level 55.000000"],
                    'gpon-olt1/3':
                        ["max-frame 2550", 
                        "switchport",
                        "bridge-group 1 spanning-tree enable",
                        "flowctrl TX",
                        "storm-control multicast level 45.000000",
                        "mirror egress destination gpon-olt1/5",
                        "no mirror egress"]} 
#**************************************************************************
config_Senario_5 = {'total':["bridge 1 protocol rstp",
                     "spanning-tree bridge 1 pathcost method short",
                     "spanning-tree bridge 1 portfast bpdu-guard"],
                    'ge1/3':
                        ["speed 10G",
                        "max-frame 1850",
                        "description",
                        "switchport",
                        "bridge-group 1 spanning-tree enable",
                        "spanning-tree edgeport",
                        "spanning-tree bpdu-guard enable",
                        "mirror both destination interface gpon-olt1/1",
                        "no mirror both"], 
                    'ge1/4':[
                        "speed 1G"
                        "max-frame 1650",
                        "switchport",
                        "bridge-group 1 spanning-tree enable"
                        "spanning-tree bpdu-filter disable",
                        "spanning-tree bpdu-guard enable",
                        "spanning-tree autoedge"],
                    'ge1/5':
                        ["speed 10G",
                        "max-frame 2050", 
                        "description",
                        "switchport",
                        "bridge-group 1 spanning-tree enable",
                        "spanning-tree edgeport",
                        "spanning-tree bpdu-guard enable",
                        "no bridge-group 1"]}
