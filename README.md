***************************************************
# Reliable File Transfer Protocol over UDP

**Eric Voong (20778118)**  
**CS 436 Winter 2023**  
**Assignment 02**

---

## Description

This program implements a reliable file transfer protocol over UDP, enabling the reliable transfer of a text file from one host to another.

## Parameters

### `sender.py`

It requires five command line inputs in the following order:
1. `<host address of the receiver>`
2. `<UDP port number used by the receiver to receive data from the sender>`
3. `<UDP port number used by the sender to send data and receive ACKs from the receiver>`
4. `<timeout interval in milliseconds>`
5. `<name of the file to be transferred>`

### `receiver.py`

It requires three command line inputs in the following order:
1. `<UDP port number used by the receiver to receive data from the sender>`
2. `<drop probability>`
3. `<name of the file into which the received data is written>`

## Usage

Log in to two different Ubuntu hosts from your laptop/desktop.

### Running the Receiver

On the first host, run the receiver using:
```sh
python3 receiver.py <UDP port number used by the receiver to receive data from the sender> <drop probability> <name of the file into which the received data is written>
```

### Running the Sender

On the second host, run the sender using:
```sh
python3 sender.py <host address of the receiver> <UDP port number used by the receiver to receive data from the sender> <UDP port number used by the sender to send data and receive ACKs from the receiver> <timeout interval in milliseconds> <name of the file to be transferred>
```

## Example Execution

1. On the first host (`host1`):
    ```sh
    python3 receiver.py 9994 0.5 <output file>
    ```
2. On the second host (`host2`):
    ```sh
    python3 sender.py host1 9994 9992 50 <input file>
    ```
