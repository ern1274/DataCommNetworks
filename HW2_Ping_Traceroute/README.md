# Ping and Traceroute Module

This module focuses on a ping program that
sends packets to the server to echo a reply
and a traceroute program to google.com with
packets being sent with an increasing ttl per hop


Required Dependencies:
* Scapy 
  * (Downloaded through PyPi or pip using command `pip install scapy`)

Modules to compile and run:
* my_ping.py
* my_traceroute.py

Compile and run module Instructions:
* Note: if you are already in the directory of the module to run
  * `python my_ping.py [-options]`
  * `python my_traceroute.py [-options]`
* Windows:
  * `python <path-to-file>\my_ping.py [-options]`
  * `python <path-to-file>\my_traceroute.py [-options]`
* Linux/Mac:
  * `python <path-to-file>/my_ping.py [-options]`
  * `python <path-to-file>/my_traceroute.py [-options]`

-Ping Options:
* `-c [num-of-packets to receive]`
* `-i [num-of-sec to wait before sending each packet]`
* `-s [packet size]`
* `-t [timeout in seconds, to stop ping]`
-Traceroute Options:
* `-n [Print hop addresses numerically]`
* `-q [nqueries, set the number of probes per TTL]`
* `-S [Summary of how many probes unanswered for each hop]`

Examples of Command Line Usage:

Ping:
* `python my_ping.py`
* `python my_ping.py -c 5`
* `python my_ping.py -i 1.5`
* `python my_ping.py -s 112`
* `python my_ping.py -t 5`
* `python my_ping.py -c 6 -i 3.2 -s 76`
Traceroute:
* `python my_traceroute.py`
* `python my_traceroute.py -n`
* `python my_traceroute.py -S`
* `python my_traceroute.py -S -n`
* `python my_traceroute.py -q 3`
* `python my_traceroute.py -q 4 -S`
* `python my_traceroute.py -q 2 -S -n`


