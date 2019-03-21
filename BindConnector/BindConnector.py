from flask import current_app as ca
import logging
import subprocess
import shlex
import os

import logging
logger = logging.getLogger('Bind-API::' + __name__ + ' ')

nsupdate_create_template = '''\
server {0}
zone {1}
update add {2}.{1} {3} A {4}
send\
'''

nsupdate_delete_template = '''\
server {0}
update delete {1} A
send
update delete {1} PTR
send\
'''

cwd = os.path.dirname(os.path.realpath(__file__))
default_ttl = '8640'
default_ns = '127.0.0.1'
default_ns_cmd = 'nsupdate'
default_sig_key = os.path.join(cwd, 'update_hosteurope_de.key')

class NSUpdateWrapper(object):

    def delete(self, params):
        logger.info('Deleting {0}'.format(params))
        return True,True

    def write_tmp(self, data):
        with open('/tmp/foo.test', 'w') as f:
            f.write(data)

    def run(self, nsaction=None, nstype=None, params=None):
        ca.logger.info("nsaction: {0}".format(nsaction))
        ca.logger.info("nstype: {0}".format(nstype))
        ca.logger.info("params: {0}".format(params))

        if nsaction == 'ADD':
            if nstype == 'A':
                cmd = nsupdate_create_template.format(
                    default_ns,
                    params.get('domain'),
                    params.get('host'),
                    params.get('ttl') if params.get('ttl', 0) != 0 else default_ttl,
                    params.get('pointsTo')
                )

        elif nsaction == 'DEL':
            if nstype == 'A':
                 cmd = nsupdate_delete_template.format(
                    default_ns,
                    params.get('domain'),
                    params.get('host'),
                    options.ttl,
                    params.get('ip')
                )

        else:
            raise TypeError('Unsupported nsaction!')


        ca.logger.debug('nsupdate cmd: {0}'.format(cmd))

        self.write_tmp(cmd)

        cmd = '{0} -k {1} {2}'.format(
            default_ns_cmd,
            default_sig_key,
            '/tmp/foo.test'
        )
        ca.logger.info("Running command: {0}".format(cmd))

        p = subprocess.run(
            shlex.split(cmd),
            universal_newlines=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=10
        )

        return p.returncode, p.stdout

nsup = NSUpdateWrapper()

def add_A(**kwargs):
    ca.logger.debug("Adding / Updating A-Record: {0}".format(kwargs.get('body')))
    data = kwargs.get('body')[0]

    ret, stdout = nsup.run(
        nsaction='ADD',
        nstype=data.get('type', 'A'),
        params=data
    )
    return [ret, stdout]

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