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
Unconfig_Senario_1 = {'total':["no bridge 1 protocol ieee"],
                    'gponolt1':
                    ["no bridge-group 1 spanning-tree enable",
                     "no switchport",
                     "no description",
                     "no flowctrl tx",
                     "no max-frame 1850"],
                    'gponolt2':
                    ["no bridge-group 1 spanning-tree disable",
                    "no switchport",
                    "no description",
                    "no flowctrl rx",
                    "no max-frame 1950"],
                    'gponolt3':
                    ["no bridge-group 1 spanning-tree enable stp",
                    "no switchport", 
                    "no max-frame 2550"]}                    

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

Unconfig_Senario_2 = {'total':["no spanning-tree bridge 1 portfast bpdu-guard",
                        "no spanning-tree bridge 1 portfast bpdu-filter",
                        "no bridge 1 protocol ieee"],
                    'ge1/1':
                    [   "no spanning-tree bpdu-guard disable",
                        "no spanning-tree bpdu-filter enable",
                        "no bridge-group 1 spanning-tree enable",
                        "no switchport",
                        "no max-frame 1600",
                        "nospeed 1G"],
                    'ge1/2':[
                        "no spanning-tree bpdu-guard enable",
                        "no spanning-tree bpdu-filter disable",
                        "no bridge-group 1 spanning-tree enable"
                        "no switchport",
                        "no description",
                        "no max-frame 1700",
                        "no speed 1G"],
                    'ge1/3':
                    [   "no mirror both destination interface ge1/4",
                        "no spanning-tree bpdu-guard enable",
                        "no spanning-tree bpdu-filter enable",
                        "no bridge-group 1 spanning-tree disable",
                        "no switchport",
                        "no description",
                        "no max-frame 1800", 
                        "no speed 10G"]}

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