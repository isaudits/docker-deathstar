# docker-deathstar

Docker implementation for automated domain admin using:
* https://github.com/EmpireProject/Empire
* https://github.com/byt3bl33d3r/DeathStar
* https://github.com/lgandx/Responder
* https://github.com/SecureAuthCorp/impacket/blob/master/examples/ntlmrelayx.py
* https://github.com/byt3bl33d3r/CrackMapExec

## Description

Based upon attack scenarios described by byt3bl33d3r:
* https://byt3bl33d3r.github.io/automating-the-empire-with-the-death-star-getting-domain-admin-with-a-push-of-a-button.html
* https://byt3bl33d3r.github.io/practical-guide-to-ntlm-relaying-in-2017-aka-getting-a-foothold-in-under-5-minutes.html
* https://byt3bl33d3r.github.io/getting-the-goods-with-crackmapexec-part-1.html
* https://byt3bl33d3r.github.io/getting-the-goods-with-crackmapexec-part-2.html

## Usage

Build

    ./build.sh

Run

    ./deathstar.sh
    
Or, alias the commands in aliases to your .bash_aliases (kali) or .bash_profile (osx) and launch with alias 'deathstar < options >'

    source /path/to/docker-deathstar/aliases

    
Options

    usage: deathstar [-h] [-d] [-v] [--no-relay] [--no-deathstar]
                         [host_ip] [target_ip]
    
    Empire / DeathStar / Responder / NTLMRelayX automation script
    
    positional arguments:
      host_ip         Host IP
      target_ip       Target IP / Range / Subnet (nmap format)
    
    optional arguments:
      -h, --help      show this help message and exit
      -d, --debug     Print lots of debugging statements
      -v, --verbose   Be verbose
      --no-relay      Disable Responder / NTLMRelayX spoofing and relaying
      --no-deathstar  Disable Deathstar autopwn

--------------------------------------------------------------------------------

Copyright 2018

Matthew C. Jones, CPA, CISA, OSCP, CCFE

IS Audits & Consulting, LLC - <http://www.isaudits.com/>

TJS Deemer Dana LLP - <http://www.tjsdd.com/>

--------------------------------------------------------------------------------

Except as otherwise specified:

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program. If not, see <http://www.gnu.org/licenses/>.