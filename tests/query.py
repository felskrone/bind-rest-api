#!/usr/bin/python3

import requests
import sys
import logging
import json
import pprint
import ast

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)


def run_add(domain=None, rtype=None, host=None, **options):
    api = 'http://127.0.0.1:9090/v0.0.2/dns/add/{domain}/{rtype}/{host}'
    headers = {'content-type': 'application/json'}
    api_url = api.format(**{'domain': domain, 'rtype': rtype, 'host': host} )
    logger.info(api_url)
    logger.info(options)
    httpsreq = requests.post(
        url=api_url,
        data=json.dumps(options.get('options')),
        headers=headers
    )
    if httpsreq.status_code == 200:
        logger.info(pprint.pprint(ast.literal_eval(httpsreq.text)))
    else:
        logger.error('{0}: {1}'.format(httpsreq.status_code, httpsreq.text))

def run_del(domain=None, rtype=None, host=None, **options):
    headers = {'content-type': 'application/json'}
    api = 'http://127.0.0.1:9090/v0.0.2/dns/delete/{domain}/{rtype}/{host}'
    api_url = api.format(**{'domain': domain, 'rtype': rtype, 'host': host})

    logger.info(api_url)
    logger.info(options)
    httpsreq = requests.post(
        url=api_url,
        data=json.dumps(options.get('options')),
        headers=headers
    )

    if httpsreq.status_code == 200:
        logger.info(pprint.pprint(ast.literal_eval(httpsreq.text)))
    else:
        logger.error('{0}: {1}'.format(httpsreq.status_code, httpsreq.text))


def run_get(domain=None):

    api_get_int = 'http://127.0.0.1:9090/v0.0.2/dns/getzone?domain={domain}'
    api_url = api_get_int.format(**{'domain': domain})
    logger.info(api_url + 'foo')
    httpsreq = requests.get(
        url=api_url
    )

    if httpsreq.status_code == 200:
        logger.info(pprint.pprint(ast.literal_eval(httpsreq.text)))
    else:
        logger.error('{0}: {1}'.format(httpsreq.status_code, httpsreq.text))

if __name__ == '__main__':

# ZONE
    run_get(domain='hosteurope.de')
#    input("Press Enter to continue...")
#    run_del(domain='hosteurope.de', rtype='A', host='vs666', options ={"pointsTo": "198.51.100.42", "ttl":100})
#    input("Press Enter to continue...")


# A
#    run_add(domain='hosteurope.de', rtype='A', host='vs666', options={"pointsTo": "198.51.100.42", "ttl": 100})
#    input("Press Enter to continue...")
#    run_del(domain='hosteurope.de', rtype='A', host='vs666', options ={"pointsTo": "198.51.100.42", "ttl":100})
#    input("Press Enter to continue...")

# MX
#    run_add(domain='hosteurope.de', rtype='MX', host='mx666', options={"pointsTo": "1.2.2.2", "priority": 200})
#    input("Press Enter to continue...")
#
#    run_add(domain='hosteurope.de', rtype='MX', host='mx667', options={"pointsTo": "1.3.3.3", "priority": 100})
#    input("Press Enter to continue...")
#    run_del(domain='hosteurope.de', rtype='MX', host='mx666', options={'pointsTo':'1.2.3.4', 'priority': 201})
#    input("Press Enter to continue...")

# TXT
#    run_add(domain='hosteurope.de', rtype='TXT', host='txt666', options={"data": "mytesttext3"})
#    input("Press Enter to continue...")
#    run_del(domain='hosteurope.de', rtype='TXT', host='txt666', options={'data':'mytesttext3'})
#    input("Press Enter to continue...")

# SRV
#    run_add(domain='hosteurope.de', rtype='SRV', host='srv666', options={
#        "priority": 100,
#        "protocol":"tcp",
#        "service":"srvtest.hosteurope.de",
#        "weight":100,
#        "port":10,
#        "target": "string.hosteurope.de"
#    })
#    input("Press Enter to continue...")
#    run_del(domain='hosteurope.de', rtype='SRV', host='srv666', options={
#        "priority": 100,
#        "protocol":"tcp",
#        "service":"srvtest.hosteurope.de",
#        "weight":100,
#        "port":10,
#        "target": "string.hosteurope.de"
#    })
#    input("Press Enter to continue...")

# CNAME
#    run_add(domain='hosteurope.de', rtype='CNAME', host='cname', options={"pointsTo": "fertig.hosteurope.de", "ttl": 100})
#    input("Press Enter to continue...")
#    run_del(domain='hosteurope.de', rtype='CNAME', host='cname', options={"pointsTo": "fertig.hosteurope.de", "ttl":100})
#    input("Press Enter to continue...")

# NS
#    run_add(domain='hosteurope.de', rtype='NS', host='nsv1', options={"pointsTo": "1.2.3.42", "ttl": 100})
#    input("Press Enter to continue...")
#    run_del(domain='hosteurope.de', rtype='NS', host='nsv1', options={"pointsTo": "1.2.3.42", "ttl":100})
#    input("Press Enter to continue...")

# SPFM
#    run_add(domain='hosteurope.de', rtype='SPF', host='hspfm', options={"spfRules": "-all"})
#    input("Press Enter to continue...")
#    run_del(domain='hosteurope.de', rtype='SPF', host='hspfm', options={"spfRules": "-all"})




