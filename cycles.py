import json
import logging
import requests
from scapy.all import ARP, sniff

logging.basicConfig()
log = logging.getLogger('cycles')
log.setLevel(logging.DEBUG)


def handle_click(button):
    cycle = button.get('cycle')
    index = button.get('index', -1) + 1
    index = index % len(cycle)
    button['index'] = index

    for url in cycle[index]:
        url = button.get('zone_url') + url
        try:
            log.debug('sending %s', url)
            r = requests.get(url)
        except:
            log.exception('requests exception')
        else:
            if r.status_code != requests.codes.ok:
                log.error('http request returned: %s', r)


def handle_arp(pkt):
    if pkt[ARP].op == 1:    # who-has (request)
        if pkt[ARP].psrc == '0.0.0.0':  # ARP Probe
            button = buttons.get(pkt[ARP].hwsrc)
            if button:
                log.info('Pushed %s', button.get('zone'))
                handle_click(button)
            else:
                log.info('ARP Probe from unknown device: %s', pkt[ARP].hwsrc)


buttons = {}
with open('config.json') as f:
    buttons = json.load(f)

# json.dump(buttons, sys.stdout, indent=4, default=lambda obj: None)

# loop forever
# requires root
sniff(prn=handle_arp, filter='arp', store=0)
