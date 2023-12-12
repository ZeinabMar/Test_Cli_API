import iperf3

ser = iperf3.Server()
ser.bind_address = '172.20.2.80'
while True:
    ser.run()