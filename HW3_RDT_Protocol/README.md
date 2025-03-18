# Reliable Data Transfer Module

This module focuses on a reliable udp data transfer program that
sends packets to the receiver to reply with acknowledgements
and a intermediary program to monitor and faciliate possible
losses or corruption in packets

reliable_data_transfer.py sets up three programs simultaneously 
as the sender, intermediary/router and receiver. The sender
is given predefined data which is hard coded to string representations
of numbers 0 - 74

file_transfer_rdt.py sets up a sender and receiver acting as a client and server.
The sender is given a hard coded file name whose file is provided in this zip file
and encodes it into chunks (predefined length) of data to be sent to the receiver. 
The receiver then returns the packets once reordered and is assembled and 
saved to the server/directory. 
Feel free to change the hard coded file name and provide your own file for testing.


Required Dependencies:
No external dependencies as all the imports are from built-in python libraries such as
* threading
* time
* zlib
* socket
* random
* multiprocessing

Modules to compile and run:
* reliable_data_transfer.py
* file_transfer_rdt.py

Compile and run module Instructions:
* Note: if you are already in the directory of the module to run
  * `python reliable_data_transfer.py`
  * `python file_transfer_rdt.py`
* Windows:
  * `python <path-to-file>\reliable_data_transfer.py`
  * `python <path-to-file>\file_transfer_rdt.py`
* Linux/Mac:
  * `python <path-to-file>/reliable_data_transfer.py [-options]`
  * `python <path-to-file>/file_transfer_rdt.py [-options]`

Examples of Command Line Usage:
* `python reliable_data_transfer.py`
* `python file_transfer_rdt.py`


