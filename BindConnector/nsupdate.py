import logging
import subprocess
import shlex
import os
from flask import current_app as ca

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
default_tt = '8640'
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

        if nsaction == 'ADD':
            if nstype == 'A':
                cmd = nsupdate_create_template.format(
                    default_ns,
                    params.get('domain'),
                    params.get('host'),
                    params.get('ttl', default_tt),
                    params.get('ip')
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


        ca.logger.debug(cmd)
        return True

        self.write_tmp(update)

        cmd = '{0} -k {1} {2}'.format(
            options.nsupdate_command,
            options.sig_key,
            '/tmp/foo.test'
        )
        logger.debug("Running command: {0}".format(cmd))

        p = subprocess.run(
            shlex.split(cmd),
            universal_newlines=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=10
        )

        return p.returncode, p.stdout

