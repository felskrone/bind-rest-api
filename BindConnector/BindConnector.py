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
nsupdate_srvrecord_template = '''\
update {2} {3}.{4}.{1} {5} SRV {6} {7} {8} {9}
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

    def delete(self, params):
        logger.info('Deleting {0}'.format(params))
        return True,True

    def write_tmp(self, data):
        with open('/tmp/foo.test', 'w') as f:
            f.write(data)

    def run(self, nsaction=None, nstype=None, params=None):

        # {'rtype': 'A', 'domain': 'hosteurope.de', 'host': 'vs6', 'body': {'ttl': 100, 'pointsTo': '198.51.100.42'}}

        ca.logger.info(params)
        ca.logger.info("nstype: {0}".format(nstype))
        ca.logger.info("params: {0}".format(params))

        if nsaction in nsactions: #translate actions coming from the API to what nsupdate understands
            if nstype in ('A', 'AAAA', 'CNAME', 'NS', 'TXT'):
                tmp = nsupdate_begin_template + nsupdate_gen_record_template + nsupdate_commit_template
                cmd = tmp.format(
                    default_ns,
                    params.get('domain'),
                    nsaction,
                    params.get('host'),
                    params.get('body').get('ttl') if params.get('ttl', 0) != 0 else default_ttl,
                    nstype,
                    params.get('body').get('pointsTo')
                )

            if nstype == "MX":
                tmp = nsupdate_begin_template + nsupdate_mxrecord_template + nsupdate_commit_template
                cmd = tmp.format(
                    default_ns,
                    params.get('domain'),
                    nsaction,
                    params.get('host'),
                    params.get('body').get('ttl') if params.get('ttl', 0) != 0 else default_ttl,
                    params.get('body').get('priority'),
                    params.get('body').get('pointsTo')
                )

            if nstype == "SRV":
                tmp = nsupdate_begin_template + nsupdate_srvrecord_template + nsupdate_commit_template
                cmd = tmp.format(
                    default_ns,
                    params.get('service'),
                    nsaction,
                    params.get('protocol'),
                    params.get('TTL') if params.get('ttl', 0) != 0 else default_ttl,
                    params.get('priority'),
                    params.get('weight'),
                    params.get('port'),
                    params.get('target')
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

        return p.returncode, p.stdout, p.stderr


nsup = NSUpdateWrapper()

def add_record(**kwargs):
    ca.logger.debug("Adding / Updating Record: {0}".format(kwargs))
    retcode, stdout, stderr = nsup.run(nsaction='add', nstype=kwargs.get('rtype'), params=kwargs)
    ca.logger.info('retcode:{0} stdout:{1} stderr:{2}'.format(retcode, stdout, stderr))

    if retcode == 0:
        return 200
    else:
        return 400 + int(retcode)


def add_records(**kwargs):
    ca.logger.debug("Adding / Updating Records: {0}".format(kwargs))
    return str(kwargs)

def del_record(**kwargs):
    ca.logger.debug("Deleting Record: {0}".format(kwargs))
    return str(kwargs)

def get_record(**kwargs):
    ca.logger.debug("Retrieving Record: {0}".format(kwargs))
    return str(kwargs)

def get_records(**kwargs):
    ca.logger.debug("Retrieving Records: {0}".format(kwargs))
    return str(kwargs)




