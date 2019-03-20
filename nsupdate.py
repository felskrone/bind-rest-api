import logging
import subprocess
import shlex
import os

from tornado.options import define, options

import logging
logger = logging.getLogger('Bind-API::' + __name__ + ' ')

nsupdate_create_template = '''\
server {0}
zone {1}
update add {2}.{1} {3} A {4}
send\
'''
nsupdate_create_ptr = '''\
update add {0} {1} PTR {2}
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
define('ttl', default='8640', type=int, help='Default TTL')
define('nameserver', default='127.0.0.1', type=str, help='Master DNS')
define('nsupdate_command', default='nsupdate', type=str, help='nsupdate')
define('sig_key', default=os.path.join(cwd, 'update_hosteurope_de.key'), type=str, help='DNSSEC Key')

class NSUpdateWrapper(object):

    def __init__(self):
        print("initing...")

    def update(self, params):

        cmd = nsupdate_create_template.format(
            options.nameserver,
            params.get('domain'),
            params.get('host'),
            options.ttl,
            params.get('ip')
        )

        return self._nsupdate(cmd)


    def delete(self, params):
        logger.info('Deleting {0}'.format(params))
        return True,True

    def write_tmp(self, data):
        with open('/tmp/foo.test', 'w') as f:
            f.write(data)

    def _nsupdate(self, update):

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

