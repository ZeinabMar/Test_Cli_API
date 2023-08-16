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


data_config(2, "bridge 1 protocol provider-rstp-edge ageing-time 100 forward-time 28 hello-time 1 max-age 7 max-hops 20 priority 8192", 
result_find=["bridge 1 protocol provider-rstp-edge" ,
 "bridge 1 ageing-time 100",
 "bridge 1 forward-time 28",
 "bridge 1 hello-time 1",
 "bridge 1 max-age 7",
 "bridge 1 max-hops 20",
 "bridge 1 priority 8192"],grep="bridge"),
 ]


bridge_custom = [
data_config(1, "bridge 1 protocol ieee-vlan-bridge ageing-time 100 forward-time 28 hello-time 1 max-age 7 max-hops 20 priority 8192", 
result_find=["bridge 1 protocol ieee-vlan-bridge" ,
 "bridge 1 ageing-time 100",
 "bridge 1 forward-time 28",
 "bridge 1 hello-time 1",
 "bridge 1 max-age 7",
 "bridge 1 max-hops 20",
 "bridge 1 priority 8192"],grep="bridge"),
]


bridge_service = [
data_config(1, "bridge 1 protocol provider-rstp ageing-time 100 forward-time 120 hello-time 1 max-age 7 max-hops 20 priority 8192", 
result_find=["bridge 1 protocol ieee-vlan-bridge" ,
 "bridge 1 ageing-time 100",
 "bridge 1 forward-time 28",
 "bridge 1 hello-time 1",
 "bridge 1 max-age 7",
 "bridge 1 max-hops 20",
 "bridge 1 priority 8192"],grep="bridge"),
]
bridge_definition_DELETE = data_config(1, "no bridge 1", 
result_not_find=["bridge 1"],grep= "bridge")
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
result_find=["vlan 17 bridge 1 type service-rooted-multipoint state enable"],grep="vlan"),
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
Switch_Enable = [data_config(1, "switchport", result_find=["switchport"], grep="switchport"),
                 data_config(1, "bridge-group 1 spanning-tree enable", result_find=["bridge-group 1 spanning-tree enable"], grep="bridge-group")]
Switch_Disable = [data_config(1, "no bridge-group 1 spanning-tree disable", result_not_find=["bridge-group 1 spanning-tree"], grep="bridge-group"),
                  data_config(1, "no switchport", result_find=["no switchport"], grep="switchport")]
#*************************************************************************************************************************************
Qos_Enable = data_config(1, "qos enable", result_find=["qos enable"],grep="qos")
Qos_Disable = data_config(1, "qos disable", result_find=["qos disable"],grep="qos")
#*************************************************************************************************************************************
Qos_Class_Config = [
 data_config(1, "class-map B match vlan 10-11", result_find=["class-map B match vlan  10-11"], grep="class-map"),
 data_config(3, "class-map C match vlan 10", result_find=["class-map C match vlan  10"], grep="class-map")]

Qos_Class_Config_Delete = [
 data_config(7, "no class-map C", result_not_find=["class-map C match"], grep="class-map"),
 data_config(8, "no class-map B", result_not_find=["class-map B match"], grep="class-map"),
]
#*************************************************************************************************************************************
Qos_policy_Config = []
Qos_policy_Config_Delete = []
#*************************************************************************************************************************************
QinQ_Registration_Table = [
data_config(1, "registration table reg1 bridge 1 cvlan 10 svlan 14", result_find=["registration table reg1 bridge 1 cvlan 10,  svlan 14,"], grep="registration"),
data_config(2, "registration table reg2 bridge 1 cvlan 10,12 svlan 14,16", result_find=["registration table reg2 bridge 1 cvlan 10, 12,  svlan 14, 16,"], grep="registration"),
data_config(3, "registration table reg3 bridge 1 cvlan 10 svlan 14", result_find=["registration table reg3 bridge 1 cvlan 10,  svlan 14,"], grep="registration"),
data_config(4, "registration table reg4 bridge 1 cvlan 10,12 svlan 14,16", result_find=["registration table reg4 bridge 1 cvlan 10, 12,  svlan 14, 16,"], grep="registration"),
data_config(5, "registration table reg5 bridge 1 cvlan 11 svlan 15", result_find=["registration table reg5 bridge 1 cvlan 11,  svlan 15,"], grep="registration"),
data_config(6, "registration table reg5 bridge 1 cvlan 10,11 svlan 14,15", result_find=["registration table reg5 bridge 1 cvlan 10,11,  svlan 14,15"], grep="registration"),
]

QinQ_Registration_Table_Delete = [
data_config(1, "no registration table reg1 bridge 1", result_not_find=[" registration table reg1"], grep="registration"),
data_config(2, "no registration table reg2 bridge 1", result_not_find=[" registration table reg2"], grep="registration"),
data_config(3, "no registration table reg3 bridge 1", result_not_find=[" registration table reg3"], grep="registration"),
data_config(4, "no registration table reg4 bridge 1", result_not_find=[" registration table reg4"], grep="registration"),
data_config(5, "no registration table reg5 bridge 1", result_not_find=[" registration table reg5"], grep="registration"),
data_config(6, "no registration table reg6 bridge 1", result_not_find=[" registration table reg6"], grep="registration"),

]
#*************************************************************************************************************************************

Bridge_Mstp_Instance_Config_Data = [
data_config(1, "spanning-tree bridge 1 mstp instance 4 vlan 10,12", result_find=["spanning-tree bridge 1 mstp instance 4 vlan 10,12,"], grep="spanning-tree bridge"),
data_config(2, "spanning-tree bridge 1 mstp instance 2 vlan 11,13" ,result_find=["spanning-tree bridge 1 mstp instance 2 vlan 11,13,"], grep="spanning-tree bridge"),
]
Bridge_Mstp_Instance_Config_Delete = [
data_config(1, "no spanning-tree bridge 1 mstp instance 2", result_not_find=["spanning-tree bridge 1 mstp instance 2"], grep="spanning-tree bridge"),
data_config(2, "no spanning-tree bridge 1 mstp instance 4", result_not_find=["spanning-tree bridge 1 mstp instance 4"], grep="spanning-tree bridge"),
]
#*************************************************************************************************************************************
