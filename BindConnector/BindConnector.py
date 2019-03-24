from flask import current_app as ca
import os
import logging
import subprocess
import shlex

logger = logging.getLogger('Bind-API::' + __name__ + ' ')

### nsupdate templates
nsupdate_begin_template = '''\
server {0}
zone {1}
\
'''

# {1} = domain, {2} = action, {3} = host, {4} = TTL, {5} = nstype {6} = pointsTo
nsupdate_gen_record_template = '''\
update {2} {3}.{1} {4} {5} {6}
\
'''

# {1} = domain, {2} = action, {3} = host, {4} = TTL, {5} = priority, {6} = pointsTo
nsupdate_mxrecord_template = '''\
update {2} {3}.{1} {4} MX {5} {6}
\
'''

# {1} = name, {2} = action,  {3} = service, {4} = protocol, {5} = TTL, {6} = priority, {7} = weight, {8} = port, {9} = target
# _ts3._udp.ts.meinedomain.de 86400 0 5 9987 ts.meinedomain.de
nsupdate_srvrecord_template = '''\
update {2} {3}.{1} {4} SRV {5} {6} {7} {8}
\
'''

nsupdate_commit_template = '''\
send\
'''
### /nsupdate templates


cwd = os.path.dirname(os.path.realpath(__file__))
default_ttl = '86400' #change this to something useful for your needs
default_ns = '127.0.0.1' #the ip bind is running on
default_ns_cmd = 'nsupdate' #nsupdate binary - change appropriately if not in path
default_sig_key = os.path.join(cwd, 'update_hosteurope_de.key') #specify the key here for updating the zones/domains
nsactions = ['add', 'del'] #nsupdate only knows either add or delete


class NSUpdateWrapper(object):

    def __init__(self, **options):
        self.options = options
        self.ttl = options.get('default_ttl', default_ttl)
        self.ns = options.get('default_ns', default_ns)

        if 'Bind' in self.options:
            self.nscmd = self.options.get('Bind').get('nscmd', default_ns_cmd)
            self.nskey = self.options.get('Bind').get('keyfile', default_sig_key)

    def delete(self, params):
        logger.info('Deleting {0}'.format(params))
        return True,True

    def write_tmp(self, data):
        with open('/tmp/foo.test', 'w') as f:
            f.write(data)

    def run(self, nsaction=None, nstype=None, params=None):

        ca.logger.debug("nsaction: {0} nstype:{1} params:{2}".format(nsaction, nstype, params))

        if nsaction in nsactions: #translate actions coming from the API to what nsupdate understands
            if nstype in ('A', 'AAAA', 'CNAME', 'NS', 'TXT', 'SPF'):

                # the actual data fields are named differently depending on the record
                if nstype == 'A' or nstype == 'CNAME' or nstype == 'NS':
                    data = params.get('body').get('pointsTo')
                elif nstype == 'TXT':
                    data = params.get('body').get('data')
                elif nstype == 'SPF':
                    data = params.get('body').get('spfRules')
                else:
                    raise ValueError('Missing data-field in record-data: {0}'.format(params))

                tmp = nsupdate_begin_template + nsupdate_gen_record_template + nsupdate_commit_template
                cmd = tmp.format(
                    self.ns,
                    params.get('domain'),
                    nsaction,
                    params.get('host'),
                    params.get('body').get('ttl') if params.get('body').get('ttl', 0) != 0 else self.ttl,
                    nstype,
                    data
                )

            elif nstype == "MX":
                tmp = nsupdate_begin_template + nsupdate_mxrecord_template + nsupdate_commit_template

                cmd = tmp.format(
                    self.ns,
                    params.get('domain'),
                    nsaction,
                    params.get('host'),
                    params.get('body').get('ttl') if params.get('body').get('ttl', 0) != 0 else self.ttl,
                    params.get('body').get('priority'),
                    params.get('body').get('pointsTo')
                )

            elif nstype == "SRV":
                tmp = nsupdate_begin_template + nsupdate_srvrecord_template + nsupdate_commit_template
                cmd = tmp.format(
                    self.ns,
                    params.get('domain'),
                    nsaction,
                    params.get('body').get('protocol'),
                    params.get('body').get('ttl') if params.get('body').get('ttl', 0) != 0 else self.ttl,
                    params.get('body').get('priority'),
                    params.get('body').get('weight'),
                    params.get('body').get('port'),
                    params.get('body').get('target')
                )
            else:
                raise TypeError('Unsupported nstype!')

        else:
            raise TypeError('Unsupported nsaction!')

        ca.logger.debug('nsupdate cmd: {0}'.format(cmd))

        self.write_tmp(cmd)

        cmd = '{0} -k {1} {2}'.format(
            self.nscmd,
            self.nskey,
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

        return p.returncode, p.stdout, p.stderr