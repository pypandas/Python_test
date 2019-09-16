from scapy.all import *
import logging

from scapy.layers.inet import IP, TCP

logging.getLogger('scapy.runtime').setLevel(logging.ERROR)

# target_ip = '101.132.118.250'
# target_port = 1801
# data = 'GET / HTTP/1.0 \r\n\r\n'

# global sport, s_seq, d_seq
# ans = sr1(IP(dst=target_ip) / TCP(dport=target_port, sport=RandShort(), seq=RandInt(), flags='S'), verbose=False)
# sport = ans[TCP].dport
# s_seq = ans[TCP].ack
# d_seq = ans[TCP].seq + 1
# send(IP(dst=target_ip) / TCP(dport=target_port, sport=sport, ack=d_seq, seq=s_seq, flags='A'), verbose=False)


s = IP(src="192.168.0.108", dst="101.132.118.250")/TCP()
print(s.show())
