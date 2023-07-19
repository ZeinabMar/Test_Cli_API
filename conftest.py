import pytest
from collections import namedtuple
import logging
from collections import namedtuple

Test_Target = 'shelf_olt'
data_config = namedtuple('data_config', ['Index', 'config', "result_find", "result_error", 'result_not_find', 'grep'])
data_config.__new__.__defaults__ = (None, "", [], [], [], "")

bridge_service_custom = [
 data_config(1, "bridge 1 protocol provider-mstp-edge ageing-time 100 forward-time 30 max-age 6 max-hops 20 priority 4096", 
 result_find=["bridge 1 protocol provider-mstp-edge" ,
 "bridge 1 ageing-time 100",
 "bridge 1 forward-time 30",
 "bridge 1 hello-time 2",
 "bridge 1 max-age 6",
 "bridge 1 max-hops 20",
 "bridge 1 priority 4096"],grep="bridge"),


data_config(2, "bridge 1 protocol provider-rstp-edge ageing-time 100 forward-time 120 hello-time 1 max-age 7 max-hops 20 priority 8192", 
result_find=["bridge 1 protocol provider-rstp-edge" ,
 "bridge 1 ageing-time 100",
 "bridge 1 forward-time 28",
 "bridge 1 hello-time 1",
 "bridge 1 max-age 7",
 "bridge 1 max-hops 20",
 "bridge 1 priority 8192"],result_error =["Problem"],grep="bridge"),
 ]

bridge_definition_DELETE = [
data_config(1, "no bridge 1", 
result_not_find=["bridge 1"],grep= "bridge")]
#**************************************************************************************************************************************

Vlan_Custom = [
data_config(1, "vlan 10 bridge 1 type customer state enable", 
result_find=["vlan 10 bridge 1 type customer state enable"],grep="vlan"),
data_config(2, "vlan 11 bridge 1 type customer state enable", 
result_find=["vlan 11 bridge 1 type customer state enable"],grep="vlan"),
data_config(3, "vlan 12 bridge 1 type customer state enable", 
result_find=["vlan 12 bridge 1 type customer state enable"],grep="vlan"),
data_config(4, "vlan 13 bridge 1 type customer state enable", 
result_find=["vlan 13 bridge 1 type customer state enable"],grep="vlan")
]

Vlan_Custom_DELETE = [
data_config(1, "no vlan 10 bridge 1 type customer", 
result_not_find=["vlan 10 bridge 1 type customer state enable"],grep= "vlan"),
data_config(2, "no vlan 11 bridge 1 type customer", 
result_not_find=["vlan 11 bridge 1 type customer state enable"],grep= "vlan"),
data_config(3, "no vlan 12 bridge 1 type customer", 
result_not_find=["vlan 12 bridge 1 type customer state enable"],grep= "vlan"),
data_config(4, "no vlan 13 bridge 1 type customer", 
result_not_find=["vlan 13 bridge 1 type customer state enable"],grep= "vlan")]

Vlan_Service = [
data_config(1, "vlan 14 bridge 1 type service-point-point state enable", 
result_find=["vlan 14 bridge 1 type service-point-point state enable"],grep="vlan"),
data_config(2, "vlan 15 bridge 1 type service-rooted-multipoint state enable", 
result_find=["vlan 15 bridge 1 type service-rooted-multipoint state enable"],grep="vlan"),
data_config(3, "vlan 16 bridge 1 type service-point-point state enable", 
result_find=["vlan 16 bridge 1 type service-point-point state enable"],grep="vlan"),
data_config(4, "vlan 17 bridge 1 type service-rooted-multipoint state enable", 
result_find=["vlan 17 bridge 1 service-rooted-multipoint state disable"],grep="vlan"),
]

Vlan_Service_DELETE = [
data_config(1, "no vlan 14 bridge 1 type service-point-point", 
result_not_find=["vlan 14 bridge 1 type service-point-point state enable"],grep= "vlan"),
data_config(2, "no vlan 15 bridge 1 type service-rooted-multipoint", 
result_not_find=["vlan 15 bridge 1 type service-rooted-multipoint state enable"],grep= "vlan"),
data_config(3, "no vlan 16 bridge 1 type service-point-point", 
result_not_find=["vlan 16 bridge 1 type service-point-point state enable"],grep= "vlan"),
data_config(4, "no vlan 17 bridge 1 type service-rooted-multipoint", 
result_not_find=["vlan 17 bridge 1 type service-rooted-multipoint state enable"],grep= "vlan"),
]
#*************************************************************************************************************************************
Switch_Enable = [Switch(1, "switchport", result_find=["switchport"], grep="switchport"),
                 Switch(1, "bridge-group 1 spanning-tree enable", result_find=["bridge-group 1 spanning-tree enable"], grep="bridge-group")]
Switch_Disable = [Switch(1, "no bridge-group 1 spanning-tree disable", result_not_find=["bridge-group 1 spanning-tree"], grep="bridge-group"),
                  Switch(1, "no switchport", result_find=["no switchport"], grep="switchport")]
#*************************************************************************************************************************************
#*************************************************************************************************************************************
QinQ_Registration_Table = [
QinQ_Registration(1, "registration table reg1 bridge 1 cvlan 10 svlan 14", result_find=["registration table reg1 bridge 1 cvlan 10,  svlan 14,"], grep="registration"),
QinQ_Registration(2, "registration table reg2 bridge 1 cvlan 10,12 svlan 14,16", result_find=["registration table reg2 bridge 1 cvlan 10, 12,  svlan 14, 16,"], grep="registration"),
QinQ_Registration(3, "registration table reg3 bridge 1 cvlan 10 svlan 14", result_find=["registration table reg3 bridge 1 cvlan 10,  svlan 14,"], grep="registration"),
QinQ_Registration(4, "registration table reg4 bridge 1 cvlan 10,12 svlan 14,16", result_find=["registration table reg4 bridge 1 cvlan 10, 12,  svlan 14, 16,"], grep="registration"),
QinQ_Registration(5, "registration table reg5 bridge 1 cvlan 11 svlan 15", result_find=["registration table reg5 bridge 1 cvlan 10, 12,  svlan 14, 16,"], grep="registration"),
]

QinQ_Registration_Table_Delete = [
QinQ_Registration(1, "no registration table reg1 bridge 1", result_not_find=[" registration table reg1"], grep="registration"),
QinQ_Registration(2, "no registration table reg2 bridge 1", result_not_find=[" registration table reg2"], grep="registration"),
QinQ_Registration(3, "no registration table reg3 bridge 1", result_not_find=[" registration table reg3"], grep="registration"),
QinQ_Registration(4, "no registration table reg4 bridge 1", result_not_find=[" registration table reg4"], grep="registration"),
QinQ_Registration(5, "no registration table reg5 bridge 1", result_not_find=[" registration table reg5"], grep="registration"),
]
#*************************************************************************************************************************************

