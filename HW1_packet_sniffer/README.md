# Packet Sniffer Module

This module focuses on sniffing packets
from Wireshark whose packets are stored in a local directory.
The capabilities of this module including filtering packets 
using libpcap/tcpdump filter format and displaying packet headers


Required Dependencies:
* Pyshark 
  * (Downloaded through PyPi or pip using command `pip install Pyshark`)
* config.py
  * Holds the absolute path to the cap_packets folder (folder that holds captured packets file)
  * Is not necessary if captured packets file is in same directory as the module
    * In which case: the `import config` can be deleted or commented out and `cap_folder_name = config.cap_folder_name` can be changed to `cap_folder_name = ""`

Modules to compile and run:
* pktsniffer.py

Compile and run module Instructions:
* Note: if you are already in the directory of the module to run
  * `python pktsniffer.py <captured-packet-file-name> [-options]`
* Windows:
  * `python <path-to-file>\pktsniffer.py <captured-packet-file-name> [-options]`
* Linux/Mac:
  * `python <path-to-file>/pktsniffer.py <captured-packet-file-name> [-options]`

-Options:
* `-c [num-of-packets]`
* Mutually Exclusive Type Qualifiers:
    * `-host [address]`
    * `-port [portnum]`
    * `-net [netaddress]`
* Mutually Exclusive Proto Qualifiers:
    * `-ip`
    * `-tcp`
    * `-udp`
    * `-icmp`

Examples of Command Line Usage:

* `python pktsniffer.py pkt1.pcapng`

* `python pktsniffer.py pkt1.pcapng -c 10`

* `python pktsniffer.py pkt1.pcapng -host 192.168.0.1`

* `python pktsniffer.py pkt1.pcapng -c 10 -port 17580 -tcp`

* `python pktsniffer.py pkt1.pcapng -host 192.168.0.1 -ip`

* `python pktsniffer.py pkt1.pcapng -net 192.168.0.1`

* `python pktsniffer.py pkt1.pcapng -tcp`

* `python pktsniffer.py pkt1.pcapng -udp`

* `python pktsniffer.py pkt1.pcapng -icmp`

