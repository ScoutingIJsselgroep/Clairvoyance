import socket
import json
import sys

# TCP_IP = '178.32.217.139'
# TCP_PORT = 3002
TCP_IP = "127.0.0.1"
TCP_PORT = 1337
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.recv(BUFFER_SIZE)

# [<puzzle name>. <puzzle as list>]
# puzzle_data = ["Tokyo Hotel", ['ABCDB EBFCG', 'AGHHD EEBAD', 'IIAFH EDJIB', 'AJFEH EDHFG', 'AJIIH EIFFJ', 'ABHJA EEAII']]
# puzzle_data = ["Tokyo Hotel", ['ABCDB EBFCG', 'AGHHD EEBAD', 'IIAFH EDJIB', 'AJFEH EDHFG', 'AJIIH EIFFJ', 'ABHJA EEAII']]
# puzzle_data = ["Snelrecht", ['ABCDE DDCFD', 'ACGEF DDCDE', 'HHBAG DEECB', 'AICDB DHBAE', 'AGBHH DEJHE',
#'AIJHI DDGAE']]
# puzzle_data = ["Snelrecht", ['ABCD DDCF', 'ACGE DDCD', 'HHBA DEEC', 'AICD DHBA', 'AGBH DEJH',  'AIJH DDGA']]
# old_solution = ["1703 4760", "1955 4471", "2216 4382", "1864 4356", "1822 4266", "1758 4412"]


# Test with coordinated in 2022
puzzle_data = [
    "2022",
    ["AHCB DHDI", "BJFA DFDG", "BAAB DDEE", "AIAG DCFB", "AFGG DCCA", "AGBG DECA"],
]

request = json.dumps([puzzle_data])

print("Sending: " + request)
s.send(request)

print("Solution: " + s.recv(1024))
s.close()