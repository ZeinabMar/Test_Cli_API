
import iperf3
import os

server = iperf3.Server()
server.bind_address = '172.20.2.80'
server.port = 5201
server.verbose = False
while True:
     server.run()