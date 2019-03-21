#!/usr/bin/env python3

import connexion
import BindConnector
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

if __name__ == '__main__':
    app = connexion.App(__name__, port=9090, specification_dir='openapi/')
    app.app.logger.addHandler(logger)
    app.app.logger.setLevel(logging.DEBUG)
    app.add_api('binddc01.yaml', arguments={'title': 'DomainConnect for Bind9+ 0.1'})
    app.run()
