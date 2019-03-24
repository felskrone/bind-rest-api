from flask import current_app as ca
from BindConnector.BindConnector import NSUpdateWrapper
from PDNSConnector.PDNSConnector import PDNSWrapper

class RequestHandler(object):
    '''
    Abstracts the request from flask into a generic handler that takes care
    of instantiating the correct backend and possible othe checks.
    '''

    backend = None
    dnswrap = None

    def __init__(self, current_app, **options):
        self.options = options

        self.backend = self.options.get('backend', 'bind')
        ca.logger.info('Using backend {0}'.format(self.backend))

        if self.backend == 'bind':
            self.dnswrap = NSUpdateWrapper(**options)
        elif self.backend == 'pdns':
            self.dnswrap = PDNSWrapper(**options)

    def handle_error(self, retcode, stdout, stderr):
        # We always get a retcode, but not necessarily any data in stdout/stderr. Return what
        # we have and add a generic error message if we dont have any error in stdout
        if retcode == 0:
            if len(stderr) >= 0:
                return [200, stdout]
        else:
            if len(stderr) >= 0:
                return [400 + int(retcode), stderr]
            else:
                return [400 + int(retcode), 'Failed to apply changes!']


    # ADD records to DNS
    def add_record(self, provider=None, **kwargs):
        ca.logger.debug("Adding / Updating Record: {0}".format(kwargs))
        try:
            retcode, stdout, stderr = self.dnswrap.run(nsaction='add', nstype=kwargs.get('rtype'), params=kwargs)
        except TypeError:
            return [500, 'Failed to execute opersation!']

        return self.handle_error(retcode, stdout, stderr)

    def add_records(self, **kwargs):
        ca.logger.debug("Adding / Updating Records: {0}".format(kwargs))
        try:
            retcode, stdout, stderr = self.dnswrap.run(nsaction='add', nstype=kwargs)
        except TypeError as exec_err:
            return [500, 'Connector failed to execute: {0}'.format(exec_err)]

        return self.handle_error(retcode, stdout, stderr)

    # DELETE records from DNS
    def del_record(self, **kwargs):
        ca.logger.debug("Deleting Record: {0}".format(kwargs))
        try:
            retcode, stdout, stderr = self.dnswrap.run(nsaction='del', nstype=kwargs.get('rtype'), params=kwargs)
        except TypeError as exec_err:
            return [500, 'Connector failed to execute: {0}'.format(exec_err)]

        return self.handle_error(retcode, stdout, stderr)

    def del_records(self, **kwargs):
        ca.logger.debug("Deleting Record: {0}".format(kwargs))
        retcode = 412
        stdout = "not handled"
        stderr = "not handled"
        return self.handle_error(retcode, stdout, stderr)


    # GET records from DNS
    def get_record(self, **kwargs):
        ca.logger.debug("Retrieving Record: {0}".format(kwargs))
        retcode = 412
        stdout = "not handled"
        stderr = "not handled"
        return self.handle_error(retcode, stdout, stderr)

    def get_entry(self, **kwargs):
        return get_record(kwargs)

    def get_zone(self, **kwargs):
        ca.logger.debug("Retrieving Zone: {0}".format(kwargs))
        retcode = 413
        stdout = "not handled"
        stderr = "not handled"
        return self.handle_error(retcode, stdout, stderr)



reqhandler = RequestHandler(ca.config)

def add_record(**kwargs):
    ca.logger.info(kwargs)
    return reqhandler.add_record(**kwargs)

def add_records(**kwargs):
    return reqhandler.add_records(**kwargs)

def del_record(**kwargs):
    return reqhandler.del_record(**kwargs)

def get_record(**kwargs):
    return reqhandler.get_record(**kwargs)

def get_records(**kwargs):
    return reqhandler.get_record(**kwargs)

def get_zone(**kwargs):
    return reqhandler.get_zone(**kwargs)