import iperf3

ser = iperf3.Server()
ser.bind_address = '172.20.2.80'
while True:
    ser.run()


# import re

# # output = """
# # Connecting to host 9.10.21.01, port 5201
# # [  4] local 9.17.201.011 port 44466 connected to 9.10.21.01 port 5201
# # [ ID] Interval           Transfer     Bandwidth       Retr  Cwnd
# # [  4]   0.00-2.00   sec  1.71 GBytes  7.36 Gbits/sec  264    789 KBytes
# # [  4]   2.00-4.00   sec  1.63 GBytes  6.99 Gbits/sec  133    865 KBytes
# # [  4]   4.00-5.00   sec   732 MBytes  6.14 Gbits/sec   11    826 KBytes
# # - - - - - - - - - - - - - - - - - - - - - - - - -
# # [ ID] Interval           Transfer     Bandwidth       Retr
# # [  4]   0.00-5.00   sec  4.06 GBytes  6.97 Gbits/sec  408             sender
# # [  4]   0.00-5.00   sec  4.05 GBytes  6.96 Gbits/sec                  receiver
# # """ 
# output = client.run()
# receiver_line = re.search(r'([\d.]+-[\d.]+)\s+sec\s+([\d.]+\s+\w?Bytes)\s+([\d.]+\s+\w?bits/sec)\s+receiver', output)
# if receiver_line:
#     interval, transfer, bandwidth = receiver_line.groups()
#     output_yaml = f"Interval: {interval}\nTransfer: {transfer}\nBandwidth: {bandwidth}"
#     print(output_yaml)
# else:
#     print("Receiver data not found in the output.")  

from datadog import initialize, statsd
import time
import iperf3
import os

# Set vars
# Remote iperf server IP
remote_site = '172.20.2.80'
# Datadog API Key
api_key = '<enter dd api key here>'
# How long to run iperf3 test in seconds
test_duration = 20

# Set DD options for statsd init
# options = {
#     'statsd_host': '127.0.0.1',
#     'statsd_port': 8125,
#     'api_key': api_key
# }
# initialize(**options)

# Set Iperf Client Options
# Run 10 parallel streams on port 5201 for duration w/ reverse
client = iperf3.Client()
client.server_hostname = remote_site
client.zerocopy = True
client.verbose = False
client.reverse = True
client.port = 5201
client.num_streams = 10
client.duration = int(test_duration)
client.bandwidth = 1000000000

# Run iperf3 test
result = client.run()

# extract relevant data
sent_mbps = int(result.sent_Mbps)
received_mbps = int(result.received_Mbps)
