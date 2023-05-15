
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
                                      "service-port 1 gemport 1 user-vlan vlan transparent",
                                      "remote service 1 gem 1 uni veip vlan-mode access pvlan vlan priority 7"],
                    'total':[
                             "bridge 1 protocol rstp-vlan-bridge", 
                             "spanning-tree bridge 1 pathcost method short", 
                             "spanning-tree bridge 1 portfast bpdu-guard",
                             "vlan 111 bridge 1 type customer state enable",
                             "vlan 112 bridge 1 type customer state enable",
                             "vlan 113 bridge 1 type customer state enable",
                             "vlan 114 bridge 1 type customer state enable",
                             "vlan 115 bridge 1 type customer state enable",
                             "vlan 116 bridge 1 type customer state enable",
                             "vlan 117 bridge 1 type customer state enable",
                             "vlan 118 bridge 1 type customer state enable",
                             "vlan 119 bridge 1 type customer state enable",
                             "vlan 220 bridge 1 type customer state enable",
                             "vlan 221 bridge 1 type customer state enable",
                             "vlan 222 bridge 1 type customer state enable"],
                    'gpon-olt':
                            ["no shutdown",
                            "switchport",
                            "bridge-group 1 spanning-tree enable",
                            "storm-control broadcast level 85",
                            "switchport mode trunk",
                            "switchport trunk tag 111-119,220-222"
                            ],
                    'ge':
                            ["max-frame 1650", 
                            "switchport",
                            "bridge-group 1 spanning-tree enable", 
                            "storm-control broadcast level 85",
                            "switchport mode trunk",
                            "switchport trunk tag 111-119,220-222",
                            "spanning-tree bpdu-filter enable",
                            "speed 1G"]}
#*******************************************************************************   
config_Service_2 = {'gpon-onu': ["tcont 1 profile test",
                                      "gemport 1 tcont 1",
                                      "service-port 1 gemport 1 user-vlan vlan transparent",
                                      "remote service 1 gem 1 uni veip vlan-mode access pvlan vlan priority 7"],
                    'total':["bridge 1 protocol rstp-vlan-bridge", 
                             "spanning-tree bridge 1 pathcost method short", 
                             "spanning-tree bridge 1 portfast bpdu-guard",
                             "vlan 111 bridge 1 type customer state enable",
                             "vlan 112 bridge 1 type customer state enable",
                             "vlan 113 bridge 1 type customer state enable",
                             "vlan 114 bridge 1 type customer state enable",
                             "vlan 115 bridge 1 type customer state enable",
                             "vlan 116 bridge 1 type customer state enable",
                             "vlan 117 bridge 1 type customer state enable",
                             "vlan 118 bridge 1 type customer state enable",
                             "vlan 119 bridge 1 type customer state enable",
                             "vlan 220 bridge 1 type customer state enable",
                             "vlan 221 bridge 1 type customer state enable",
                             "vlan 222 bridge 1 type customer state enable"],
                    'gpon-olt':
                            ["no shutdown",
                            "switchport",
                            "bridge-group 1 spanning-tree enable",
                            "storm-control broadcast level 85",
                            "switchport mode trunk",
                            "switchport trunk tag 111-119,220-222"
                            ],
                    'ge1/1':
                            ["max-frame 1650", 
                            "switchport",
                            "bridge-group 1 spanning-tree enable", 
                            "storm-control broadcast level 85",
                            "switchport mode trunk",
                            "switchport trunk tag 111-116",
                            "spanning-tree bpdu-filter enable"],
                    "ge1/2" :[
                            "speed 1G",
                            "max-frame 1650",
                            "switchport", 
                            "bridge-group 1 spanning-tree enable",
                            "storm-control broadcast level 85",
                            "switchport mode trunk",
                            "switchport trunk tag 117-119,220-222",
                            "spanning-tree bpdu-guard enable"]}        
#****************************************************************************************************
config_Service_3 = {'gpon-onu': ["tcont 1 profile test",
                                      "gemport 1 tcont 1",
                                      "service-port 1 gemport 1 user-vlan vlan transparent",
                                      "remote service 1 gem 1 uni veip vlan-mode access pvlan vlan priority 7"],
                    'total':[
                # "bridge 1 protocol provider-rstp-edge", 
                #              "spanning-tree bridge 1 pathcost method short", 
                #              "spanning-tree bridge 1 portfast bpdu-guard",
                #              "vlan 111 bridge 1 type customer state enable",
                #              "vlan 112 bridge 1 type customer state enable",
                #              "vlan 113 bridge 1 type customer state enable",
                #              "vlan 114 bridge 1 type customer state enable",
                #              "vlan 115 bridge 1 type customer state enable",
                #              "vlan 11 bridge 1 type service-point-point state enable",
                #              "vlan 12 bridge 1 type service-point-point state enable",
                #              "vlan 13 bridge 1 type service-point-point state enable",
                #              "vlan 14 bridge 1 type service-point-point state enable",
                #              "vlan 15 bridge 1 type service-point-point state enable",
                             "registration table reg1 bridge 1 cvlan 112, 111, 114, 113, 115,  svlan 12, 11, 14, 13, 15,"],
                    'gpon-olt':
                            ["no shutdown",
                            "switchport",
                            "bridge-group 1 spanning-tree enable",
                            "switchport mode customer-edge-trunk",
                            "switchport QinQ trunk mode C-tagged tag 111-115 egresstag enable",
                            "switchport QinQ registration reg1"
                            ],
                    'ge':
                            ["switchport",
                            "bridge-group 1 spanning-tree enable", 
                            "switchport mode customer-network",
                            "switchport QinQ trunk mode S-tagged tag 11-15",
                            "speed 1G"]}   
#**********************************************************************************************************
config_Service_4 = {'gpon-onu': ["tcont 1 profile test",
                                      "gemport 1 tcont 1",
                                      "service-port 1 gemport 1 user-vlan vlan transparent",
                                      "remote service 1 gem 1 uni veip vlan-mode access pvlan vlan priority 7"],
                    'total':["bridge 1 protocol provider-rstp-edge", 
                             "vlan 111 bridge 1 type customer state enable",
                             "vlan 112 bridge 1 type customer state enable",
                             "vlan 113 bridge 1 type customer state enable",
                             "vlan 114 bridge 1 type customer state enable",
                             "vlan 115 bridge 1 type customer state enable",
                             "vlan 11 bridge 1 type service-point-point state enable",
                             "vlan 12 bridge 1 type service-point-point state enable",
                             "vlan 13 bridge 1 type service-point-point state enable",
                             "vlan 14 bridge 1 type service-point-point state enable",
                             "vlan 15 bridge 1 type service-point-point state enable",
                             "vlan 16 bridge 1 type service-point-point state enable",
                             "vlan 17 bridge 1 type service-point-point state enable",
                             "vlan 18 bridge 1 type service-point-point state enable",
                             "vlan 19 bridge 1 type service-point-point state enable",
                             "vlan 20 bridge 1 type service-point-point state enable",
                             "registration table reg1 bridge 1 cvlan 112,111,114,113,115 svlan 12,11,14,13,15"],
                    'gpon-olt':
                            ["no shutdown",
                            "switchport",
                            "bridge-group 1 spanning-tree enable",
                            "switchport mode customer-edge-trunk",
                            "switchport QinQ trunk mode C-tagged tag 111-115 egresstag enable",
                            "switchport QinQ registration reg1"
                            ],
                    'ge':
                            ["speed 1G",
                            "switchport",
                            "bridge-group 1 spanning-tree enable", 
                            "switchport mode customer-network",
                            "switchport QinQ trunk mode S-tagged tag 11-15",
                            "switchport QinQ trunk translation svlan-src 16,17,18,19,20 svlan-des 11,12,13,14,15"]}   
#***************************************************************************************************************************    
config_Service_5 = {'gpon-onu': ["tcont 1 profile HSI",
	                         "gemport 1 tcont 1",
	                         "service-port 1 gemport 1 user-vlan 111 transparent",
	                         "remote service 1 gem 1 uni veip vlan-mode access pvlan 111 priority 7",
	                         "tcont 2 profile VOIP",
	                         "gemport 2 tcont 2",
	                         "service-port 2 gemport 2 user-vlan 121 transparent",
	                         "remote service 2 gem 2 uni veip vlan-mode access pvlan 121 priority 7"],
                    'total':["bridge 1 protocol provider-rstp-edge", 
                             "vlan 111 bridge 1 type customer state enable",
                             "vlan 121 bridge 1 type customer state enable"],
                    'gpon-olt':
                            ["no shutdown",
                            "switchport",
                            "bridge-group 1 spanning-tree enable",
                            "switchport mode trunk",
                            "switchport trunk tag 111,121"],
                    'ge':
                           ["switchport",
                            "bridge-group 1 spanning-tree enable", 
                            "speed 1G",
                            "switchport mode trunk",
                            "switchport trunk tag 111,121"]}                                                                                                                                                                                             
#****************************************************************************************************************************
config_Service_6 = {'gpon-onu': ["tcont 1 profile test",
	                         "gemport 1 tcont 1",
	                         "service-port 1 gemport 1 user-vlan 111 transparent",
	                         "remote service 1 gem 1 uni veip vlan-mode access pvlan 111 priority 7"],
                    'total':["bridge 1 protocol rstp-vlan-bridge", 
                             "lacp priority 50",
                             "vlan 111 bridge 1 type customer state enable"],
                    'gpon-olt':
                            ["no shutdown",
                            "switchport",
                            "bridge-group 1 spanning-tree enable",
                            "switchport mode trunk",
                            "switchport trunk tag 111"],
                    'ge':
                           ["switchport",
                            "bridge-group 1 spanning-tree enable", 
                            "speed 1G",
                            "switchport mode trunk",
                            "switchport trunk tag 111",
                            "channel-group 5 mode active"]}   
#****************************************************************************************************************************
config_Service_8 = {'gpon-onu': [
                                "onu-srvprofile profile-id id onu-type STG-402",
	                        "tcont 1 profile test",
	                        "gemport 1 tcont 1",
	                        "service-port 1 gemport 1 user-vlan vlan transparent",
	                        "remote service 1 gem 1 uni veip vlan-mode access pvlan vlan priority 7"],
                    'total':["bridge 1 protocol rstp-vlan-bridge", 
                             "lacp priority 50",
                             "vlan 111 bridge 1 type customer state enable",
                             "vlan 112 bridge 1 type customer state enable",
                             "vlan 113 bridge 1 type customer state enable",
                             "vlan 114 bridge 1 type customer state enable",
                             "vlan 115 bridge 1 type customer state enable",
                             "vlan 116 bridge 1 type customer state enable",
                             "vlan 117 bridge 1 type customer state enable",
                             "vlan 118 bridge 1 type customer state enable",
                             "vlan 119 bridge 1 type customer state enable",
                             "vlan 220 bridge 1 type customer state enable",
                             "vlan 221 bridge 1 type customer state enable",
                             "vlan 222 bridge 1 type customer state enable"],
                    'gpon-olt':
                            ["no shutdown",
                            "multi-onusrv-cfg onu-srvprofile id onu 1-6",
                            "switchport",
                            "bridge-group 1 spanning-tree enable",
                            "switchport mode trunk",
                            "switchport trunk tag 111-119,220-222"],
                    'ge':
                           ["speed 1G",
	                    "max-frame 1650", 
	                    "switchport", 
	                    "bridge-group 1 spanning-tree enable", 
	                    "switchport mode trunk",
	                    "switchport trunk tag 111-119,220-222"]} 
#we dont allow to exit gpon and set onu 
# these two setting are applied togethor as unique setting which are shown in above as gpon_onu
# **********************************************************************************************************************************                            
config_Service_9 = {'gpon': ["protectgroup 1 name test workpon gpon-olt1/1 protectpon gpon-olt1/2 typeB",
	                     "protectgroup 1 state enable"],
                    'gpon-onu': [
                                "onu-srvprofile profile-id id onu-type STG-402",
	                        "tcont 1 profile test",
	                        "gemport 1 tcont 1",
	                        "service-port 1 gemport 1 user-vlan vlan transparent",
	                        "remote service 1 gem 1 uni veip vlan-mode access pvlan vlan priority 7"],
                    'total':["bridge 1 protocol provider-rstp-edge", 
                             "vlan 111 bridge 1 type customer state enable",
                             "vlan 112 bridge 1 type customer state enable",
                             "vlan 113 bridge 1 type customer state enable",
                             "vlan 114 bridge 1 type customer state enable",
                             "vlan 115 bridge 1 type customer state enable"],
                    'gpon-olt':
                            ["no shutdown",
                            "switchport",
                            "bridge-group 1 spanning-tree enable",
                            "switchport mode trunk",
                            "switchport trunk tag 111-115"],
                    'ge':
                           ["speed 1G",
	                    "max-frame 1650", 
	                    "switchport", 
	                    "bridge-group 1 spanning-tree enable", 
	                    "switchport mode trunk",
	                    "switchport trunk tag 111-115"]} 
                        