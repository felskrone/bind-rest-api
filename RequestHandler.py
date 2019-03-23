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
            self.dnswrap = NSUpdateWrapper()
        elif self.backend == 'pdns':
            self.dnswrap = PDNSWrapper(options)

    def add_record(self, provider=None, **kwargs):
        ca.logger.debug("Adding / Updating Record: {0}".format(kwargs))
        retcode, stdout, stderr = self.dnswrap.run(nsaction='add', nstype=kwargs.get('rtype'), params=kwargs)
        ca.logger.info('retcode:{0} stdout:{1} stderr:{2}'.format(retcode, stdout, stderr))

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

    def add_records(self, **kwargs):
        ca.logger.debug("Adding / Updating Records: {0}".format(kwargs))
        return str(kwargs)

    def del_record(self, **kwargs):
        ca.logger.debug("Deleting Record: {0}".format(kwargs))
        return str(kwargs)

    def del_records(self, **kwargs):
        ca.logger.debug("Deleting Record: {0}".format(kwargs))
        return str(kwargs)

    def get_record(**kwargs):
        ca.logger.debug("Retrieving Record: {0}".format(kwargs))
        return str(kwargs)

    def get_zone(**kwargs):
        ca.logger.debug("Retrieving Zone: {0}".format(kwargs))
        return str(kwargs)



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