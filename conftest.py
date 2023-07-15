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
