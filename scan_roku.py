#!/usr/bin/env python
import logging
import sys

from app.roku import RokuDevice, RokuError

logger = logging.getLogger('alexa-roku')


def main(ip_addr):
    try:
        roku = RokuDevice(ip_addr)
    except RokuError as e:
        sys.stderr.write('{0}\n'.format(e))
        sys.exit(2)

    # show some info
    sys.stdout.write(
        'Found your {0.model}, "{0.name}". It has the following channels:\n'
        .format(roku)
    )
    for channel in roku.channels:
        sys.stdout.write('* {0.id:>5}: {0}\n'.format(channel))

    # lookup a channel
    netflix = roku.get_channel('Netflix')
    sys.stdout.write('The Netflix channel is {0.id}.\n'.format(netflix))

    # launch Netflix
    roku.launch_channel(netflix.name)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    if len(sys.argv) != 2:
        sys.stderr.write('Usage: {0} <ip>\n'.format(sys.argv[0]))
        sys.exit(1)
    ip = sys.argv[1]
    main(ip)
