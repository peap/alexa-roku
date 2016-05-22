#!/usr/bin/env python
import sys

from app import ssdp

ST = 'ssdp:all'


def main():
    sys.stdout.write('Spending 5 seconds discovering local SSDP devices...\n')
    sys.stdout.flush()

    devices = ssdp.discover(ST)
    if devices:
        sys.stdout.write(
            'Found {0} devices:\n'
            .format(len(devices))
        )
        for device in devices:
            sys.stdout.write('--> {0}\n'.format(device))
    else:
        sys.stdout.write('Did not find any SSDP devices on your local network.')


if __name__ == '__main__':
    main()
