# docker-deathstar

## THIS PROJECT IS NO LONGER MAINTAINED DUE TO OFFICIAL DOCKER IMAGES AVAILABLE FOR DEATHSTAR AND EMPIRE

Docker implementation for automated domain admin using:
* https://github.com/byt3bl33d3r/DeathStar
* https://github.com/EmpireProject/Empire
* https://github.com/lgandx/Responder
* https://github.com/SecureAuthCorp/impacket/blob/master/examples/ntlmrelayx.py
* https://github.com/byt3bl33d3r/CrackMapExec

## Description

Based upon attack scenarios described by [byt3bl33d3r](https://github.com/byt3bl33d3r):
* https://byt3bl33d3r.github.io/automating-the-empire-with-the-death-star-getting-domain-admin-with-a-push-of-a-button.html
* https://byt3bl33d3r.github.io/practical-guide-to-ntlm-relaying-in-2017-aka-getting-a-foothold-in-under-5-minutes.html


## Runtime Notes
Components run inside of tmux windows and must be individually closed via ctrl-c / exit commands.
Closing the parent terminal will leave the docker container running in the background.
Make sure that you exit out all windows all the way down to your original command shell -
If you see the tmux statusbar at the bottom of your command window, keep typing 'exit'!

Running on OSX, the netbiosd service conflicts with listeners on UDP ports 137-138
so these ports cannot be exposed from the docker container. This limits the attacks
that Responder can leverage. Given the option, you will likely have better results
running inside of a Linux VM with bridged networking on top of OSX as opposed to
inside of a native OSX docker instance.

## Usage

Pull:

    docker pull isaudits/deathstar

or Build:

    ./build.sh

Run

    ./deathstar.sh
    
    
Options

    usage: entrypoint.py [-h] [-d] [-v] [--port PORT] [--no-relay]
                         [--no-deathstar] [--no-mimikatz] [--no-domain-privesc]
                         [host_ip] [target_ip]
    
    Empire / DeathStar / Responder / NTLMRelayX automation script
    
    positional arguments:
      host_ip               Host IP
      target_ip             Target IP / Range / Subnet (nmap format)
    
    optional arguments:
      -h, --help            show this help message and exit
      -d, --debug           Print lots of debugging statements
      -v, --verbose         Be verbose
      --port PORT, -p PORT  Port for Empire listener (8443)
      --no-relay            Disable Responder / NTLMRelayX spoofing and relaying
      --no-deathstar        Disable Deathstar autopwn
      --no-mimikatz         Do not use Mimikatz during lateral movement (default:
                            False)
      --no-domain-privesc   Do not use domain privilege escalation techniques
                            (default: False)


### Disable options
```--no-relay``` and ```no-deathstar``` flags are available to disable these components
from launching.

```--no-relay``` disables the MiTM components from Responder and NTLMRelayX, resulting in
just an Empire listener with DeathStar integrated (unless disabled with the ```--no-deathstar```
flag). Use this feature for a quick and dirty DeathStar setup without leveraging MiTM.

```--no-deathstar``` disables the DeathStar component, allowing shells to be obtained via
Empire without using DeathStar to further pivot and elevate privileges. DeathStar is initially
launched and then killed to create the listener inside of Empire, and a tmux pane is left open
so that DeathStar can be re-launched at any time by activating the DeathStar pane and hitting
the up-arrow.

Use both flags together to get a quick Empire console with the option to re-enable DeathStar
and attack atttached shells at any point in time.

```--no-mimikatz``` and ```no-domain-privesc``` flags are native DeathStar options to disable
Mimikatz and domain privilege escalation techniques, respectively.

### Quick launch via alias
You can also source the aliases file in your .bash_aliases (kali) or .bash_profile (osx)
and launch straight from terminal with alias ```deathstar <options>```

    source /path/to/docker-deathstar/aliases

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