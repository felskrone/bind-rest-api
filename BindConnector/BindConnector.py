from flask import current_app as ca
import logging
import subprocess
import shlex
import os
import logging

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
nsactions = {'ADD', 'DEL'} #nsupdate only knows either add or delete

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

        if nsaction in nsactions: #translate actions coming from the API to what nsupdate understands
            if nsaction == "ADD":
                nsaction = "add"
            else:
                nsaction = "delete"
            if nstype in ('A', 'AAAA', 'CNAME', 'NS', 'TXT'):
                tmp = nsupdate_begin_template + nsupdate_gen_record_template + nsupdate_commit_template
                cmd = tmp.format(
                    default_ns,
                    params.get('domain'),
                    nsaction,
                    params.get('host'),
                    params.get('ttl') if params.get('ttl', 0) != 0 else default_ttl,
                    nstype,
                    params.get('pointsTo')
                )

            if nstype == "MX":
                tmp = nsupdate_begin_template + nsupdate_mxrecord_template + nsupdate_commit_template
                cmd = tmp.format(
                    default_ns,
                    params.get('domain'),
                    nsaction,
                    params.get('host'),
                    params.get('ttl') if params.get('ttl', 0) != 0 else default_ttl,
                    params.get('priority'),
                    params.get('pointsTo')
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
    ca.logger.debug("Deleting A-Record: {0}".format(str(kwargs)))
    ret, stdout = nsup.run(
        nsaction='DEL',
        nstype='A',
        params=data
    )
    return [ret, stdout]

def add_AAAA(**kwargs):
    ca.logger.debug("Adding / Updating AAAA-Record: {0}".format(kwargs.get('body')))
    data = kwargs.get('body')[0]

    ret, stdout = nsup.run(
        nsaction='ADD',
        nstype=data.get('type', 'AAAA'),
        params=data
    )
    return [ret, stdout]

def del_AAAA(**kwargs):
    ca.logger.debug("Deleting AAAA-Record: {0}".format(str(kwargs)))
    ret, stdout = nsup.run(
        nsaction='DEL',
        nstype='AAAA',
        params=data
    )
    return [ret, stdout]

def add_CNAME(**kwargs):
    ca.logger.debug("Adding / Updating CNAME-Record: {0}".format(kwargs.get('body')))
    data = kwargs.get('body')[0]

    ret, stdout = nsup.run(
        nsaction='ADD',
        nstype=data.get('type', 'CNAME'),
        params=data
    )
    return [ret, stdout]

def del_CNAME(**kwargs):
    ca.logger.debug("Deleting CNAME-Record: {0}".format(str(kwargs)))
    ret, stdout = nsup.run(
        nsaction='DEL',
        nstype='CNAME',
        params=data
    )
    return [ret, stdout]

def add_NS(**kwargs):
    ca.logger.debug("Adding / Updating NS-Record: {0}".format(kwargs.get('body')))
    data = kwargs.get('body')[0]

    ret, stdout = nsup.run(
        nsaction='ADD',
        nstype=data.get('type', 'NS'),
        params=data
    )
    return [ret, stdout]

def del_NS(**kwargs):
    ca.logger.debug("Deleting NS-Record: {0}".format(str(kwargs)))
    ret, stdout = nsup.run(
        nsaction='DEL',
        nstype='NS',
        params=data
    )
    return [ret, stdout]

def add_TXT(**kwargs):
    ca.logger.debug("Adding / Updating TXT-Record: {0}".format(kwargs.get('body')))
    data = kwargs.get('body')[0]

    ret, stdout = nsup.run(
        nsaction='ADD',
        nstype=data.get('type', 'TXT'),
        params=data
    )
    return [ret, stdout]

def del_TXT(**kwargs):
    ca.logger.debug("Deleting TXT-Record: {0}".format(str(kwargs)))
    ret, stdout = nsup.run(
        nsaction='DEL',
        nstype='TXT',
        params=data
    )
    return [ret, stdout]

def add_MX(**kwargs):
    ca.logger.debug("Adding / Updating MX-Record: {0}".format(kwargs.get('body')))
    data = kwargs.get('body')[0]

    ret, stdout = nsup.run(
        nsaction='ADD',
        nstype=data.get('type', 'MX'),
        params=data
    )
    return [ret, stdout]

def del_MX(**kwargs):
    ca.logger.debug("Deleting MX-Record: {0}".format(str(kwargs)))
    ret, stdout = nsup.run(
        nsaction='DEL',
        nstype='MX',
        params=data
    )
    return [ret, stdout]

def add_Multi(**kwargs):
    for record in kwargs.get('body'):
        print("type:{0}: data:{1}".format(record.get('type', 'unknown'), record))
    return str(kwargs)


def add_SRV(**kwargs):
    ca.logger.debug("Adding / Updating SRV-Record: {0}".format(kwargs.get('body')))
    data = kwargs.get('body')[0]

    ret, stdout = nsup.run(
        nsaction='ADD',
        nstype=data.get('type', 'SRV'),
        params=data
    )
    return [ret, stdout]

def del_SRV(**kwargs):
    ca.logger.debug("Deleting SRV-Record: {0}".format(str(kwargs)))
    ret, stdout = nsup.run(
        nsaction='DEL',
        nstype='SRV',
        params=data
    )
    return [ret, stdout]