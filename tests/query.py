#!/usr/bin/python3

import requests
import sys
import logging
import json
import pprint
import ast

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)

api_add_int = 'http://127.0.0.1:9090/v0.0.2/dns/{domain}/{rtype}/{host}'

def run(method='post', domain=None, rtype=None, host=None, **options):

    headers = {'content-type': 'application/json'}
    api_url = api_add_int.format(**{'domain': domain, 'rtype': rtype, 'host': host} )
    logger.info(api_url)
    logger.info(options)

    if method == 'post':
        httpsreq = requests.post(
            url=api_url,
            data=json.dumps(options.get('options')),
            headers=headers
        )
    elif method == 'get':
        pass
    elif method == 'delete':
        httpsreq = requests.delete(
            url=api_url,
            headers=headers
        )

    if httpsreq.status_code == 200:
        logger.info(pprint.pprint(ast.literal_eval(httpsreq.text)))
    else:
        logger.error('{0}: {1}'.format(httpsreq.status_code, httpsreq.text))

if __name__ == '__main__':

# A
#    run(domain='hosteurope.de', rtype='A', host='vs6', options={"pointsTo": "198.51.100.42", "ttl": 100})
#    input("Press Enter to continue...")
#    run(method='delete', domain='hosteurope.de', rtype='A', host='vs6')
#    input("Press Enter to continue...")

# MX
    run(domain='hosteurope.de', rtype='MX', host='mx666', options={"pointsTo": "1.2.3.4", "priority": 201})
#    input("Press Enter to continue...")
#    run(method='delete', domain='hosteurope.de', rtype='MX', host='vs6')
#    input("Press Enter to continue...")

#    input("Press Enter to continue...")
#    run('A', DELA_single, 'delete')
#    input("Press Enter to continue...")
#    run('A', A_single_type)
#    input("Press Enter to continue...")
#    run('A', A_multi)
#
    #    A_single_type = [{"domain": "hosteurope.de", "host": "string", "pointsTo": "198.51.100.42", "ttl": 0, "type":"A"}]
#    A_multi = [
#        {"domain": "hosteurope.de", "host": "Astring", "pointsTo": "198.51.100.42", "ttl": 0, "type":"A"},
#        {"domain": "hosteurope.de", "host": "Bstring", "pointsTo": "198.51.100.43", "ttl": 0}]
#    DELA_single = [{"domain": "hosteurope.de", "host": "string"}]
#
#
#    TXT_single = [{"domain": "hosteurope.de", "host": "vs5", "data": "spf=xyz"}]
#    TXT_single_cf = [{"domain": "hosteurope.de", "host": "vs5", "data": "spf=xyz", "txtConflictMatchingMode":"None", "txtConflictMatchingPrefix":"test"}]
#    TXT_single_type = [{"domain": "hosteurope.de", "host": "vs5", "data": "spf=xyz", "type":"TXT"}]
#    TXT_multi = [
#        {"domain": "hosteurope.de", "host": "vs5", "data": "spf=abc", "ttl": 0},
#        {"domain": "hosteurope.de", "host": "string", "data": "spf=cde", "ttl": 0}]
#    DELTXT_single = [{"domain": "hosteurope.de", "host": "vs5", "data": "spf=xyz"}]
#
#    MX_single = [{"domain": "hosteurope.de", "host": "vs5", "pointsTo": "10.11.12.13", "ttl":100, "priority":100}]
#    MX_single_type = [{"domain": "hosteurope.de", "host": "vs5", "pointsTo": "10.11.12.13", "ttl":100, "priority":100, "type":"MX"}]
#    MX_multi = [
#        {"domain": "hosteurope.de", "host": "vs5", "pointsTo": "10.11.12.13", "ttl":100, "priority":100, "type":"MX"},
#        {"domain": "vs.de", "host": "fg5", "pointsTo": "10.15.52.53", "ttl":100, "priority":100, "type":"MX"}]
#
#    MULTI_multi = [
#        {"domain": "hosteurope.de", "host": "vs5", "data": "spf=abc", "ttl": 0, "type":"TXT"},
#        {"domain": "hosteurope.de", "host": "string", "pointsTo": "198.51.100.42", "ttl": 0, "type":"A"}
#    ]
#

## MX
#    run('MX', MX_single)
##    run('MX', MX_single_type)
##    run('MX', MX_multi)
#
## TXT
##    run('TXT', TXT_single)
##    run('TXT', TXT_single_cf)
##    run('TXT', TXT_single_type)
##    run('TXT', TXT_multi)
#
## MULTI
##    run('MULTI', MULTI_multi)
