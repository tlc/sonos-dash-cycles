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
    base  = button.get('zone_url', '')

    for url in cycle[index]:
        if base and url:
            url = base.rstrip('/') + '/' + url.lstrip('/')   # no extra /
        elif not url:
            url = base
        if not url:
            continue

        try:
            log.debug('sending %s', url)
            r = requests.get(url)
        except:
            log.exception('requests exception')
        else:
            if r.status_code != requests.codes.ok:
                log.error('http request returned: %s', r)


def handle_arp(pkt):
    if not ARP in pkt:
        return
    if pkt[ARP].op == 1:    # who-has (request)
        if pkt[ARP].psrc == '0.0.0.0':  # ARP Probe
            button = buttons.get(pkt[ARP].hwsrc)
            if button:
                log.info('Pushed %s', button.get('name'))
                handle_click(button)
            else:
                log.info('ARP Probe from unknown device: %s', pkt[ARP].hwsrc)


buttons = {}
try:
    with open('config.json') as f:
        buttons = json.load(f)
except:
    log.info("Error reading config, still discovering.")

# json.dump(buttons, sys.stdout, indent=4, default=lambda obj: None)

# loop forever
# requires root
sniff(prn=handle_arp, filter='arp', store=0)
