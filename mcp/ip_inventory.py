#!/usr/bin/env python
#
#

import sys
import yaml
import ipaddress
import argparse

HELP_EPILOG = '''
  Reads YAML from STDIN and outputs IP to minion mapping

  EXAMPLES:
    > salt '*' grains.get ipv4 --out yaml | ip_inventory.py
    > salt '*' grains.get ipv4 --out yaml | ip_inventory.py --cind 192.168.0.0/24
'''

parser = argparse.ArgumentParser(description='List IP address inventory based on Salt grains',
                                 formatter_class=argparse.RawDescriptionHelpFormatter,
                                 epilog=HELP_EPILOG)
parser.add_argument('--cidr',
                    help="Show only specified network")
parser.add_argument('--networks', action='store_true',
                    help="Show available networks")
args = parser.parse_args()

default_netmask = '/24'
# hash. keys are salt minion names
salt_out = yaml.load(sys.stdin)

#ip_inventory = {
#    IPv4Network(u'46.49.131.0/24'): {
#        IPv4Address(u'46.49.131.223'): None,
#        IPv4Address(u'46.49.131.225'): 'host1'
#    }
#}
#
inventory = {}

for minion, minion_addresses in salt_out.iteritems():
    for addr in minion_addresses:
        address = ipaddress.ip_address(unicode(addr))
        net = ipaddress.ip_network(unicode(addr + default_netmask), strict=False)
        # skip loopbacks
        if address.is_loopback:
            continue
        # add network to the inventory if it isn't there
        if net not in inventory.keys():
            inventory[net] = {}.fromkeys(list(net.hosts()))
        inventory[net][address] = minion
 
if args.networks:
    for net in inventory.iterkeys():
        print(str(net))
    sys.exit(0)
if args.cidr:
    net = ipaddress.ip_network(unicode(args.cidr), strict=False)
    ips = inventory[net].keys()
    ips.sort()
    for addr in ips:
        print('{} {}'.format(addr, inventory[net][addr]))
else:
    for net in inventory:
        print('--- Network {}'.format(net))
        ips = inventory[net].keys()
        ips.sort()
        for addr in ips:
            print('{} {}'.format(addr, inventory[net][addr]))
