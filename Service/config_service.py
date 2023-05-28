
from collections import namedtuple
gpon = namedtuple('gpon', ['name', 'fixed', 'assured', 'maximum'])
gpon.__new__.__defaults__ = ("test", 0, 0, 0)

reg = namedtuple('reg', ['name', 'cvlan', 'svlan'])
reg.__new__.__defaults__ = ("reg", [0], [0])

trans = namedtuple('trans', ['svlansrc', 'svlandes'])
trans.__new__.__defaults__ = ([0], [0])


#*********************************************************************************************************************
config_Service_1 = {'gpon-onu': [ "tcont 1 profile test",
                                      "gemport 1 tcont 1",
                                      "service-port 1 gemport 1 user-vlan vlan_number transparent",
                                      "remote service 1 gem 1 uni veip vlan-mode access pvlan vlan_number priority PI"],
                    'total':[
                             "bridge 1 protocol rstp-vlan-bridge", 
                             "spanning-tree bridge 1 pathcost method short", 
                             "spanning-tree bridge 1 portfast bpdu-guard",
                        #      "vlan 111 bridge 1 type customer state enable",
                        #      "vlan 112 bridge 1 type customer state enable",
                        #      "vlan 113 bridge 1 type customer state enable",
                        #      "vlan 114 bridge 1 type customer state enable",
                        #      "vlan 115 bridge 1 type customer state enable",
                             "vlan 116 bridge 1 type customer state enable",
                        #      "vlan 117 bridge 1 type customer state enable",
                        #      "vlan 118 bridge 1 type customer state enable",
                        #      "vlan 119 bridge 1 type customer state enable",
                        #      "vlan 220 bridge 1 type customer state enable",
                             "vlan 221 bridge 1 type customer state enable",
                             "vlan 220 bridge 1 type customer state enable"],
                    'gpon-olt1/1':
                            ["no shutdown",
                            "switchport",
                            "bridge-group 1 spanning-tree enable",
                            "storm-control broadcast level 85",
                            "switchport mode trunk",
                            "switchport trunk tag 116"
                            ],
                     'gpon-olt1/2':
                            ["no shutdown",
                            "switchport",
                            "bridge-group 1 spanning-tree enable",
                            "storm-control broadcast level 85",
                            "switchport mode trunk",
                            "switchport trunk tag 220-221"
                            ],       
                    'ge':
                            ["max-frame 1650", 
                            "switchport",
                            "bridge-group 1 spanning-tree enable", 
                            "storm-control broadcast level 85",
                            "switchport mode trunk",
                            "switchport trunk tag 116,220-221",
                            "spanning-tree bpdu-filter enable",
                            "speed 1G"]}
#*******************************************************************************   
config_Service_2 = {'gpon-onu': ["tcont 1 profile test",
                                      "gemport 1 tcont 1",
                                      "service-port 1 gemport 1 user-vlan vlan_number transparent",
                                      "remote service 1 gem 1 uni veip vlan-mode access pvlan vlan_number priority PI"],
                    'total':["bridge 1 protocol rstp-vlan-bridge", 
                             "spanning-tree bridge 1 pathcost method short", 
                             "spanning-tree bridge 1 portfast bpdu-guard",
                        #      "vlan 111 bridge 1 type customer state enable",
                        #      "vlan 112 bridge 1 type customer state enable",
                        #      "vlan 113 bridge 1 type customer state enable",
                        #      "vlan 114 bridge 1 type customer state enable",
                        #      "vlan 115 bridge 1 type customer state enable",
                             "vlan 116 bridge 1 type customer state enable",
                        #      "vlan 117 bridge 1 type customer state enable",
                        #      "vlan 118 bridge 1 type customer state enable",
                        #      "vlan 119 bridge 1 type customer state enable",
                             "vlan 220 bridge 1 type customer state enable",
                             "vlan 221 bridge 1 type customer state enable",
                        #      "vlan 222 bridge 1 type customer state enable"
                        ],
                    'gpon-olt1/1':
                            ["no shutdown",
                            "switchport",
                            "bridge-group 1 spanning-tree enable",
                            "storm-control broadcast level 85",
                            "switchport mode trunk",
                            "switchport trunk tag 116"
                            ],
                     'gpon-olt1/2':
                            ["no shutdown",
                            "switchport",
                            "bridge-group 1 spanning-tree enable",
                            "storm-control broadcast level 85",
                            "switchport mode trunk",
                            "switchport trunk tag 220-221"
                            ],       
                    'ge1/1':
                            ["speed 1G",
                            "max-frame 1650", 
                            "switchport",
                            "bridge-group 1 spanning-tree enable", 
                            "storm-control broadcast level 85",
                            "switchport mode trunk",
                            "switchport trunk tag 116",
                            "spanning-tree bpdu-filter enable"],
                    "ge1/2" :[
                            "speed 1G",
                            "max-frame 1650",
                            "switchport", 
                            "bridge-group 1 spanning-tree enable",
                            "storm-control broadcast level 85",
                            "switchport mode trunk",
                            "switchport trunk tag 220-221",
                            "spanning-tree bpdu-guard enable"]}        
#****************************************************************************************************
config_Service_3 = {'gpon-onu': ["tcont 1 profile test",
                                      "gemport 1 tcont 1",
                                      "service-port 1 gemport 1 user-vlan vlan_number transparent",
                                      "remote service 1 gem 1 uni veip vlan-mode access pvlan vlan_number priority PI"],
                    'total':[
                "bridge 1 protocol provider-rstp-edge", 
                             "spanning-tree bridge 1 pathcost method short", 
                             "spanning-tree bridge 1 portfast bpdu-guard",
                             "vlan 116 bridge 1 type customer state enable",
                             "vlan 220 bridge 1 type customer state enable",
                             "vlan 221 bridge 1 type customer state enable",
                #              "vlan 114 bridge 1 type customer state enable",
                #              "vlan 115 bridge 1 type customer state enable",
                #              "vlan 11 bridge 1 type service-point-point state enable",
                #              "vlan 12 bridge 1 type service-point-point state enable",
                             "vlan 116 bridge 1 type service-point-point state enable",
                             "vlan 220 bridge 1 type service-point-point state enable",
                             "vlan 221 bridge 1 type service-point-point state enable",
                             "registration table reg1 bridge 1 cvlan 116, 220, 221  svlan 116, 220, 221"],
                    'gpon-olt':
                            ["no shutdown",
                            "switchport",
                            "bridge-group 1 spanning-tree enable",
                            "switchport mode customer-edge-trunk",
                            "switchport QinQ trunk mode C-tagged tag 116,220-221 egresstag enable",
                            "switchport QinQ registration reg1"
                            ],
                    'ge':
                            ["switchport",
                            "bridge-group 1 spanning-tree enable", 
                            "switchport mode customer-network",
                            "switchport QinQ trunk mode S-tagged tag 116,220-221",
                            "speed 1G"]}   
#**********************************************************************************************************
config_Service_4 = {'gpon-onu': ["tcont 1 profile test",
                                      "gemport 1 tcont 1",
                                      "service-port 1 gemport 1 user-vlan vlan_number transparent",
                                      "remote service 1 gem 1 uni veip vlan-mode access pvlan vlan_number priority PI"],
                    'total':["bridge 1 protocol provider-rstp-edge", 
                             "vlan 116 bridge 1 type customer state enable",
                             "vlan 220 bridge 1 type customer state enable",
                             "vlan 221 bridge 1 type customer state enable",
                        #      "vlan 114 bridge 1 type customer state enable",
                        #      "vlan 115 bridge 1 type customer state enable",
                             "vlan 116 bridge 1 type service-point-point state enable",
                             "vlan 220 bridge 1 type service-point-point state enable",
                             "vlan 221 bridge 1 type service-point-point state enable",
                             "vlan 113 bridge 1 type service-point-point state enable",
                             "vlan 114 bridge 1 type service-point-point state enable",
                             "vlan 115 bridge 1 type service-point-point state enable",
                        #      "vlan 17 bridge 1 type service-point-point state enable",
                        #      "vlan 18 bridge 1 type service-point-point state enable",
                        #      "vlan 19 bridge 1 type service-point-point state enable",
                        #      "vlan 20 bridge 1 type service-point-point state enable",
                             "registration table reg1 bridge 1 cvlan 116,221,220 svlan 116,221,220"],
                    'gpon-olt':
                            ["no shutdown",
                            "switchport",
                            "bridge-group 1 spanning-tree enable",
                            "switchport mode customer-edge-trunk",
                            "switchport QinQ trunk mode C-tagged tag 116,220-221 egresstag enable",
                            "switchport QinQ registration reg1"
                            ],
                    'ge':
                            ["speed 1G",
                            "switchport",
                            "bridge-group 1 spanning-tree enable", 
                            "switchport mode customer-network",
                            "switchport QinQ trunk mode S-tagged tag 116,220-221",
                            "switchport QinQ trunk translation svlan-src 115,114,113 svlan-des 116,221,220"]}   
#***************************************************************************************************************************    
config_Service_5 = {'gpon-onu': ["tcont 1 profile HSI",
	                         "gemport 1 tcont 1",
	                         "service-port 1 gemport 1 user-vlan 221 transparent",
	                         "remote service 1 gem 1 uni veip vlan-mode access pvlan 221 priority 7",
	                         "tcont 2 profile VOIP",
	                         "gemport 2 tcont 2",
	                         "service-port 2 gemport 2 user-vlan 220 transparent",
	                         "remote service 2 gem 2 uni veip vlan-mode access pvlan 220 priority 6"],
                    'total':["bridge 1 protocol provider-rstp-edge", 
                             "vlan 220 bridge 1 type customer state enable",
                             "vlan 221 bridge 1 type customer state enable"],
                    'gpon-olt':
                            ["no shutdown",
                            "switchport",
                            "bridge-group 1 spanning-tree enable",
                            "switchport mode trunk",
                            "switchport trunk tag 220-221"],
                    'ge':
                           ["switchport",
                            "bridge-group 1 spanning-tree enable", 
                            "speed 1G",
                            "switchport mode trunk",
                            "switchport trunk tag 220-221"]}                                                                                                                                                                                             
#****************************************************************************************************************************
config_Service_6 = {'gpon-onu': ["tcont 1 profile test",
	                         "gemport 1 tcont 1",
	                         "service-port 1 gemport 1 user-vlan 116 transparent",
	                         "remote service 1 gem 1 uni veip vlan-mode access pvlan 116 priority 3"],
                    'total':["bridge 1 protocol rstp-vlan-bridge", 
                             "lacp priority 50",
                             "vlan 116 bridge 1 type customer state enable"],
                    'gpon-olt':
                            ["no shutdown",
                            "switchport",
                            "bridge-group 1 spanning-tree enable",
                            "switchport mode trunk",
                            "switchport trunk tag 116"],
                    'ge':
                           ["switchport",
                            "bridge-group 1 spanning-tree enable", 
                            "speed 1G",
                            "switchport mode trunk",
                            "switchport trunk tag 116",
                            "channel-group 5 mode active"]}   
#****************************************************************************************************************************
config_Service_8 = {'gpon-onu': [
                                "onu-srvprofile profile-id pro-id onu-type STG-402",
	                        "tcont 1 profile test",
	                        "gemport 1 tcont 1",
	                        "service-port 1 gemport 1 user-vlan vlan_number transparent",
	                        "remote service 1 gem 1 uni veip vlan-mode access pvlan vlan_number priority PI"],
                    'total':["bridge 1 protocol rstp-vlan-bridge", 
                             "lacp priority 50",
                        #      "vlan 111 bridge 1 type customer state enable",
                        #      "vlan 112 bridge 1 type customer state enable",
                        #      "vlan 113 bridge 1 type customer state enable",
                        #      "vlan 114 bridge 1 type customer state enable",
                        #      "vlan 115 bridge 1 type customer state enable",
                             "vlan 116 bridge 1 type customer state enable",
                        #      "vlan 117 bridge 1 type customer state enable",
                        #      "vlan 118 bridge 1 type customer state enable",
                        #      "vlan 119 bridge 1 type customer state enable",
                             "vlan 220 bridge 1 type customer state enable",
                             "vlan 221 bridge 1 type customer state enable",
                        #      "vlan 222 bridge 1 type customer state enable"
                        ],
                    'gpon-olt1/1':
                            ["no shutdown",
                            "multi-onusrv-cfg onu-srvprofile 1 onu 1-2",
                            "switchport",
                            "bridge-group 1 spanning-tree enable",
                            "switchport mode trunk",
                            "switchport trunk tag 116"],
                     'gpon-olt1/2':
                            ["no shutdown",
                            "multi-onusrv-cfg onu-srvprofile 2 onu 1-2",
                            "switchport",
                            "bridge-group 1 spanning-tree enable",
                            "switchport mode trunk",
                            "switchport trunk tag 220-221"],       
                    'ge':
                           ["speed 1G",
	                    "max-frame 1650", 
	                    "switchport", 
	                    "bridge-group 1 spanning-tree enable", 
	                    "switchport mode trunk",
	                    "switchport trunk tag 116,220-221"]} 
#we dont allow to exit gpon and set onu 
# these two setting are applied togethor as unique setting which are shown in above as gpon_onu
# **********************************************************************************************************************************                            
config_Service_9 = {'gpon': ["protectgroup 1 name test workpon gpon-olt1/1 protectpon gpon-olt1/2 typeB",
	                     "protectgroup 1 state enable"],
                    'gpon-onu': ["tcont 1 profile test",
	                        "gemport 1 tcont 1",
	                        "service-port 1 gemport 1 user-vlan vlan_number transparent",
	                        "remote service 1 gem 1 uni veip vlan-mode access pvlan vlan_number priority PI"],
                    'total':["bridge 1 protocol rstp-vlan-bridge", 
                             "vlan 116 bridge 1 type customer state enable",
                             "vlan 220 bridge 1 type customer state enable",
                             "vlan 221 bridge 1 type customer state enable",
                        #      "vlan 114 bridge 1 type customer state enable",
                        #      "vlan 115 bridge 1 type customer state enable"
                        ],
                    'gpon-olt':
                            ["no shutdown",
                            "switchport",
                            "bridge-group 1 spanning-tree enable",
                            "switchport mode trunk",
                            "switchport trunk tag 116,220-221"],
                    'ge':
                           ["speed 1G",
	                    "max-frame 1650", 
	                    "switchport", 
	                    "bridge-group 1 spanning-tree enable", 
	                    "switchport mode trunk",
	                    "switchport trunk tag 116,220-221"]} 
                        