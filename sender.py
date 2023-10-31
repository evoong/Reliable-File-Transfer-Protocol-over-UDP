from socket import *
import os
import time
import sys



# checks for invalid parameters
if len(sys.argv) < 6:
    print ("missing parameter")
    raise SystemExit
if len(sys.argv) > 6:
    print ("too many parameter")
    raise SystemExit

if sys.argv[2].isdigit() == 0:
    print("port # is not an integer")
    raise SystemExit

if sys.argv[3].isdigit() == 0:
    print("port # is not an integer")
    raise SystemExit

if sys.argv[4].isdigit() == 0:
    print("port # is not an integer")
    raise SystemExit
if isinstance(sys.argv[5], str) == False:
    print("Expected String for file name")
    raise SystemExit


recAddress = sys.argv[1]
recPort = int(sys.argv[2])
sendPort = int(sys.argv[3])
timeLimit =  float(sys.argv[4])
fileName = sys.argv[5]

senderSocket = socket(AF_INET,SOCK_DGRAM)
senderSocket.bind(('', sendPort))
senderSocket.settimeout(1)


with open(fileName, 'r') as file:
    f = file.read()
## Parses text by every 500th character
op = [(f[i:i + 500]) for i in range(0, len(f), 500)]

packetList=[]
# PACKET FORMAT

# integer type; // 0: ACK, 1: Data, 2: EOT
# integer seqnum; // sequence number of the packet
# integer length; // Length of the String variable ‘data’
# String data; // String with Max Length 500

for i in range(0, len(op)):
    packet = "1|" + str(i) + "|" + str(len(op[i])) + "|" + str(op[i])
    packetList.append(packet)

# stores seqnum of sent packets for seqnum.log
sentPackets = []

# sends all packets
for j in packetList:
    packet = bytes(j, encoding='utf-8')
    senderSocket.sendto(packet,(recAddress, recPort))
    sentPackets.append(j.split("|")[1])

startTime = time.time()

#stores all ack seqnum received
ackPackList = []

while True:
    try:
        # listens for acks
        ackPack, serverAddress = senderSocket.recvfrom(1024)
        ackPackList.append(ackPack.decode().split("|")[1])
    except timeout:
        print("waiting")
    timeRemaining  = time.time() - startTime
    # when timeout occurs, resend all packets that were not acknowledged
    if timeRemaining >= timeLimit/1000:
        for k in packetList:
            if k.split("|")[1] not in ackPackList:
                packet = bytes(k, encoding='utf-8')
                senderSocket.sendto(packet,(recAddress, recPort))
                sentPackets.append(k.split("|")[1])

        startTime = time.time()
    # when all packets have been acknowledged, then the sender will send an EOT
    if len(ackPackList) == len(packetList):
        eot_packt= "2|0|0|"
        senderSocket.sendto(bytes(eot_packt, encoding='utf-8'), (recAddress,recPort))
        break

# program closes connection upon reciever EOT
recAckPack, serverAddress = senderSocket.recvfrom(1024)
if recAckPack.decode().split("|")[0] == "2":
    senderSocket.close()

# logs all the seqnum of all sent packets
with open("seqnum.log", "wb") as file:
    for i in sentPackets:
        file.write(bytes(i+"\n", encoding= 'utf-8'))

file.closed

# logs all the seqnum of all the acks
with open("ack.log", "wb") as file:
    for i in ackPackList:
        file.write(bytes(i+"\n", encoding= 'utf-8'))
file.closed