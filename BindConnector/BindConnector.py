from flask import current_app as ca
import os

import logging
logger = logging.getLogger('Bind-API::' + __name__ + ' ')

def add_record(**kwargs):
    ca.logger.debug("Adding / Updating Record: {0}".format(kwargs.get('body')))
    return str(kwargs)

def add_records(**kwargs):
    ca.logger.debug("Adding / Updating Records: {0}".format(kwargs.get('body')))
    return str(kwargs)

def del_record(**kwargs):
    ca.logger.debug("Deleting Record: {0}".format(str(kwargs)))
    return str(kwargs)

def get_record(**kwargs):
    ca.logger.debug("Retrieving Record: {0}".format(kwargs.get('body')))
    return str(kwargs)

def get_records(**kwargs):
    ca.logger.debug("Retrieving Records: {0}".format(kwargs.get('body')))
    return str(kwargs)
