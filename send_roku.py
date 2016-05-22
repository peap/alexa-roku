#!/usr/bin/env python
import logging
import sys

from app.roku import RokuDevice, RokuError

logger = logging.getLogger('alexa-roku')


def main(ip_addr, button):
    try:
        roku = RokuDevice(ip_addr)
    except RokuError as e:
        sys.stderr.write('{0}\n'.format(e))
        sys.exit(2)

    # show some info
    sys.stdout.write(
        'Found your {0.model}, "{0.name}". Pressing "{1}"...\n'
        .format(roku, button)
    )
    sys.stdout.flush()
    # launch Netflix
    roku.press_button(button)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    if len(sys.argv) != 3:
        sys.stderr.write('Usage: {0} <ip> <button>\n'.format(sys.argv[0]))
        sys.exit(1)
    ip, button = sys.argv[1:3]
    main(ip, button)
