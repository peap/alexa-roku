#!/usr/bin/env python
import logging

from app import app

logging.basicConfig(level=logging.INFO)
logging.getLogger('requests').setLevel(logging.WARNING)

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        sys.stderr.write('Usage: {0} host:port\n'.format(sys.argv[0]))
        sys.exit(1)
    host, port = sys.argv[1].split(':')
    sys.stdout.write('Starting server at {0}:{1}\n'.format(host, port))
    app.config.update({
        'HOST': host,
        'PORT': port,
        'DEBUG': True,
    })
    app.run(host=host, port=int(port))
