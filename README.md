# subnet.py
CLI tool to determine various information of a given IPv4 address in CIDR format.

## Installation
This program is written in Python using only the builtin libraries, you can move it
wherever you like and invoke it from there.

## Usage
Run the program without any parameter, the helper will walk you through on how to use it.
For example:

```sh
$> ./subnet.py 10.0.3.4/24
IP Address: 10.0.3.4 (00001010 00000000 00000011 00000100)
Subnet Mask: 255.255.255.0 (11111111 11111111 11111111 00000000)
Network Prefix: 10.0.3.0 (00001010 00000000 00000011 00000000)
Host Prefix: 0.0.0.4 (00000000 00000000 00000000 00000100)
Usable Hosts: 254
IP Class: A
```
