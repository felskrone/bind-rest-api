#!/usr/bin/env python3

import connexion
from nsupdate import NSUpdateWrapper
import logging
from flask import current_app as ca

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def add_A(**kwargs):
    ca.logger.debug("Adding / Updating A-Record: {0}".format(kwargs.get('body')))
    return str(kwargs)

def del_A(**kwargs):
    ca.logger.debug("Deleting A-Record: {0}".format(kwargs.get('body')))
    return str(kwargs)

def add_TXT(**kwargs):
    ca.logger.debug("Adding / Updating TXT-Record: {0}".format(kwargs.get('body')))
    return str(kwargs)

def add_MX(**kwargs):
    ca.logger.debug("Adding / Updating MX-Record: {0}".format(kwargs.get('body')))
    return str(kwargs)

def add_CNAME(**kwargs):
    ca.logger.debug("Adding / Updating MX-Record: {0}".format(kwargs.get('body')))
    return str(kwargs)

def add_Multi(**kwargs):
    for record in kwargs.get('body'):
        print("type:{0}: data:{1}".format(record.get('type', 'unknown'), record))
    return str(kwargs)

if __name__ == '__main__':
    app = connexion.App(__name__, port=9090, specification_dir='swagger/')
    app.app.logger.addHandler(logger)
    app.app.logger.setLevel(logging.DEBUG)
    app.add_api('binddc.yaml', arguments={'title': 'DomainConnect for Bind9+'})
    app.run()
