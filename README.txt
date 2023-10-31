***************************************************
Eric Voong (20778118)
CS 436 Winter 2023
Assignment 02
***************************************************


Description:
This program is uses the reliable file transfer protocol, 
which could be used to reliably transfer a text file from one 
host to another over UDP

Parameters
1.  sender.py 
    It will take five command line inputs in order:
        <host address of the receiver>
        <UDP port number used by the receiver to receive data from the sender>
        <UDP port number used by the sender to send data and receive ACKs from the receiver>
        <timeout interval in units of millisecond>
        <name of the file to be transferred>

2.  receiver.py
    It will take three command line inputs in order:
        <UDP port number used by the receiver to receive data from the sender>
        <drop probability>
        <name of the file into which the received data is written>


#Usage

Login to two different Ubuntu hosts from your laptop/desktop

Run the receiver first on the first host using:
python3 receiver <UDP port number used by the receiver to receive data from the sender>  <drop probability> <name of the file into which the received data is written>


Run sender on the second host using:
python3 sender.py <host address of the receiver> <UDP port number used by the receiver to receive data from the sender> <UDP port number used by the sender to send data and receive ACKs from the receiver>  <timeout interval in units of millisecond> <name of the file to be transferred>

#Example Execution
 
1. On the host host1: python receiver.py 9994 0.5 <output File>
2. On the host host2: python sender.py host1 9994 9992 50 <input file>

