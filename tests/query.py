#!/usr/bin/python

import requests
import sys
import logging
import json
import pprint
import ast

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)

api_add_int = 'http://127.0.0.1:9090/v0.0.1/{0}'
api_del_int = 'http://127.0.0.1:9090/v0.0.1/{0}?{1}'

def run(atype=None, data=None, operation='post'):

    headers = {'content-type': 'application/json'}

    logger.info('DELETEing record with URL {0}'.format(api_del_int.format(atype, 'arecord={0}'.format(data))))
    if operation == 'post':
        logger.info('POSTing data to URL {0}'.format(api_add_int.format(atype)))
        httpsreq = requests.post(
            url=api_add_int.format(atype),
            data=json.dumps(data),
            headers=headers
        )

    elif operation == 'delete':

        url=api_del_int.format(atype, 'host=string&domain=hosteurope.de')

        logger.info('DELETEing record with URL {0}'.format(url))

        httpsreq = requests.delete(
            url=url,
            data=json.dumps(data),
            headers=headers
        )

    if httpsreq.status_code == 200:
        logger.info(pprint.pprint(ast.literal_eval(httpsreq.text)))
    else:
        logger.error('{0}: {1}'.format(httpsreq.status_code, httpsreq.text))

if __name__ == '__main__':

    A_single = [{"domain": "hosteurope.de", "host": "string", "pointsTo": "198.51.100.42", "ttl": 0}]
    A_single_type = [{"domain": "hosteurope.de", "host": "string", "pointsTo": "198.51.100.42", "ttl": 0, "type":"A"}]
    A_multi = [
        {"domain": "hosteurope.de", "host": "string", "pointsTo": "198.51.100.42", "ttl": 0, "type":"A"},
        {"domain": "hosteurope.de", "host": "string", "pointsTo": "198.51.100.42", "ttl": 0}]


    DELA_single = [{"domain": "hosteurope.de", "host": "string"}]


    TXT_single = [{"domain": "hosteurope.de", "host": "vs5", "data": "spf=xyz"}]
    TXT_single_cf = [{"domain": "hosteurope.de", "host": "vs5", "data": "spf=xyz", "txtConflictMatchingMode":"None", "txtConflictMatchingPrefix":"test"}]
    TXT_single_type = [{"domain": "hosteurope.de", "host": "vs5", "data": "spf=xyz", "type":"TXT"}]
    TXT_multi = [
        {"domain": "hosteurope.de", "host": "vs5", "data": "spf=abc", "ttl": 0},
        {"domain": "hosteurope.de", "host": "string", "data": "spf=cde", "ttl": 0}]

    MX_single = [{"domain": "hosteurope.de", "host": "vs5", "pointsTo": "10.11.12.13", "ttl":100, "priority":100}]
    MX_single_type = [{"domain": "hosteurope.de", "host": "vs5", "pointsTo": "10.11.12.13", "ttl":100, "priority":100, "type":"MX"}]
    MX_multi = [
        {"domain": "hosteurope.de", "host": "vs5", "pointsTo": "10.11.12.13", "ttl":100, "priority":100, "type":"MX"},
        {"domain": "vs.de", "host": "fg5", "pointsTo": "10.15.52.53", "ttl":100, "priority":100, "type":"MX"}]

    MULTI_multi = [
        {"domain": "hosteurope.de", "host": "vs5", "data": "spf=abc", "ttl": 0, "type":"TXT"},
        {"domain": "hosteurope.de", "host": "string", "pointsTo": "198.51.100.42", "ttl": 0, "type":"A"}
    ]

#    run('MX', MX_single)
#    run('MX', MX_single_type)
#    run('MX', MX_multi)
#    run('A', A_single)
    run('A', DELA_single, 'delete')
#    run('A', A_single_type)
#    run('A', A_multi)
#    run('TXT', TXT_single)
#    run('TXT', TXT_single_cf)
#    run('TXT', TXT_single_type)
#    run('TXT', TXT_multi)
#    run('MULTI', MULTI_multi)
