
# SONOS DASH CYCLES

Cycles is a simple, little program that listens for Amazon Dash buttons
and sends commands to your Sonos.

The Dash button use was inspired by a
[blog post](https://medium.com/@edwardbenson/how-i-hacked-amazon-s-5-wifi-button-to-track-baby-data-794214b0bdd8).
It uses jishi's
[node-sonos-http-api](https://github.com/jishi/node-sonos-http-api) server
to talk to your Sonos.

Since the Dash button is a single action button, Cycles will cycle through
a series of preconfigured actions -- favorites, volume levels, etc.
It can be configured for multiple Dash buttons acting on 1 or more Sonos.

## Note
*Amazon Dash buttons are not fast.*  It takes about 11 seconds to detect the button press and about another 50 until another press will be accepted *by the button*.  Still, it's better than getting your phone out sometimes.

## Requirements
Install and configure [node-sonos-http-api](https://github.com/jishi/node-sonos-http-api) server.  Test it with your browser.

**_PARTIALLY_** configure your Amazon Dash button as described in Step 1
[here](https://medium.com/@edwardbenson/how-i-hacked-amazon-s-5-wifi-button-to-track-baby-data-794214b0bdd8).  You don't want to order diapers
every time you change the music.  That page also gives a nice description
of what the Dash button is doing.  Cycles can do Step 2 for you.

## Configuration
The configuration file associates MAC addresses (the colon separated number
below) with a *"name"* for logging, a base *"zone_url"* and a *"cycle"* of actions.

    {
        "f0:27:2d:e0:dc:28": {
            "name": "Gatorade Kitchen Favs",
            "zone_url": "http://localhost:6006/kitchen/",
            "cycle": [
                [ "favorite/Ska Radio", "play" ],
                [ "favorite/Angel" ],
                [ "favorite/Party Music" ],
                [ "pause" ]
                ]
        },
        ....
    }

You can determine the MAC address of the button by running Cycles,
pressing the button and waiting a few seconds for the log to print it.
Then you can start creating your config file.  Cycles expects it to
be "config.json" in the local directory.

The *"zone_url"* is the where your node-sonos-http-api server is running
(not your Sonos!) and it typically specifies which zone.
The *"cycle"* is a list of actions, which are lists of strings that will be
sequentially appended to the "zone_url" and sent to the
node-sonos-http-api server.

See the [node-sonos-http-api](https://github.com/jishi/node-sonos-http-api)
documentation for what types of cycle actions you can send.

Note the action with two strings in the configuration above.
Generally, sending a favorite/\* URL will cause Sonos to play it.  But there
is a [scenario](https://github.com/jishi/node-sonos-http-api/issues/159)
where Pandora stations don't immediately play.  Hence the two actions
in my example.

**By the way, cycles doesn't actually contain any Sonos specific behavior.
You could configure it to HTTP GET URLs for anything.**

## Execution
Cycles expects a local config.json file.  If it's not there, or doesn't parse well, Cycles will still do MAC discovery.  
Because Cycles sniffs network arp packets, it requires root permissions to run.

    sudo python cycles.py

If you prefer you can run the docker version.  The packet sniffing requires
`--net=host`

    docker run -d --restart=always --name=cycles --net=host -v $PWD/myconfig.json:/cycles/config.json troyc/sonos-dash-cycles



