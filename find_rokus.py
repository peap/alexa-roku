#!/usr/bin/env python
import sys
from urllib.parse import urlparse

from app import ssdp
from app.roku import RokuDevice

ROKU_ST = 'roku:ecp'


def main():
    sys.stdout.write('Spending 5 seconds discovering local Roku devices...\n')
    sys.stdout.flush()

    devices = ssdp.discover(ROKU_ST)
    rokus = list(filter(lambda d: d.st == ROKU_ST, devices))
    others = list(filter(lambda d: d.st != ROKU_ST, devices))

    if devices:
        sys.stdout.write(
            'Found {0} devices: {1} Rokus and {2} others.\n'
            .format(len(devices), len(rokus), len(others))
        )
    else:
        sys.stdout.write('Did not find any Rokus on your local network.')

    if rokus:
        sys.stdout.write('--> Rokus:\n')
        for device in rokus:
            parsed = urlparse(device.location)
            roku = RokuDevice(parsed.hostname, parsed.port)
            n_apps = len(roku.channels)
            sys.stdout.write('    * {0} ({0.name})\n'.format(roku))

    if others:
        sys.stdout.write('--> Others:\n')
        for device in others:
            sys.stdout.write('    * {0}\n'.format(device.location))

    if rokus:
        sys.stdout.write('Try running ./scan_roku <ip> :)\n')

if __name__ == '__main__':
    main()
