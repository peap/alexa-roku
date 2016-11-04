# alexa-roku
Use an Amazon Echo to control your Roku player.

See ASK/utterances.txt for examples of what you can do.

## Usage
Create a Python 3 virtual environment and install `requirements.txt`. Run
`server.py` on your local network, make it reachable from Amazon, and create an
Alexa Skills Kit skill to connect them.

My setup is nginx + gunicorn on a Raspberry Pi on my local network,
which has Dyn DNS service to keep a consistent hostname.

When launching the Flask server in this app, specify your Amazon Application ID
as an environment variable, `AMAZON_APPLICATION_ID`. If desired, you can also
specify the IP address of your Roku on the local network as `ROKU_ADDRESS`;
otherwise, SSDP will be used to discover it.

To find the IP address of your Roku, you can use the `find_roku.py` script
in your virtual environment.
