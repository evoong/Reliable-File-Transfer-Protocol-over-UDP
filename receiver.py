from socket import *
import random
import sys


# checks for invalid parameters

if len(sys.argv) < 4:
    print ("missing parameter")
    raise SystemExit
if len(sys.argv) > 4:
    print ("too many parameter")
    raise SystemExit

if sys.argv[1].isdigit() == 0:
    print("port # is not an integer")
    raise SystemExit

if sys.argv[2].replace(".","").isnumeric() == 0:
    print("drop probability is not an float")
    raise SystemExit

if isinstance(sys.argv[3], str) == False:
    print("Expected String for file name")
    raise SystemExit

# returns the seqnum of packet
def getKey(packet):
    return int(packet.decode().split("|")[1])

recPort = int(sys.argv[1])
dropProb = float(sys.argv[2])
saveFile = sys.argv[3]

receiverSocket = socket(AF_INET,SOCK_DGRAM)
receiverSocket.bind(('', recPort))

#buffer for received packets
receivedPackets = []

#record seqnum of received packs
seqNumList  = []

while True:
    # receives packets
    msg,senderAddress = receiverSocket.recvfrom(1024)
    print(msg.decode())

    # if packet is EOT then receiver sends EOT
    if int(msg.decode().split("|")[0]) == 2: # If type received is EOT
        eot_packt=  bytes("2|0|0|", encoding='utf-8')
        receiverSocket.sendto(eot_packt,senderAddress)
        print("sent eot")
        break

    # randonly drops packets based on probability
    if random.random() >= dropProb:
        continue

    # discards if packet is a duplicate
    elif msg.decode().split("|")[1] in seqNumList:
        continue
    else:
        # adds packets to the buffer
        receivedPackets.append(msg)
        seqNumList.append(msg.decode().split("|")[1] )
        ackPacket = "0|" + msg.decode().split("|")[1] +"|0|"
        packet = bytes(ackPacket,encoding='utf-8')
        receiverSocket.sendto(packet, senderAddress)

receiverSocket.close
# sorts buffer by seqnum
receivedPackets.sort(key=getKey)
print(receivedPackets)

# outputs the files
with open(saveFile, "wb") as file: 
    for i in receivedPackets:
        file.write(bytes(i.decode().split("|")[3], encoding='utf-8'))

file.closed





         
        