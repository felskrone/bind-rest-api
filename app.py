#!/usr/bin/env python3
import yaml
import connexion
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def run():
    try:
        with open('config.yaml', 'r') as cfg:
            config = yaml.load(cfg)
    except (IOError) as load_err:
        print("Failed to load config file")

    try:
        app = connexion.App(__name__, port=9090, specification_dir='openapi/')
        with app.app.app_context():
            app.app.config.update(config)
            app.app.logger.addHandler(logger)
            app.app.logger.setLevel(logging.DEBUG)
            app.add_api('bindrest01.yaml', arguments={'title': 'DomainConnect for Bind9+ 0.1'})
            app.run()
    except ValueError as conf_err:
        print("Failed to start service: {0}".format(conf_err))

if __name__ == '__main__':
    run()

