import dns.zone
import dns.query
import json

class SimpleAXFR(object):

    supp_types = ['TXT', 'MX', 'A', 'SOA', 'NS', 'SPF', 'CNAME']

    field_names = {
        'A': ['address'],
        'SOA': ['expire', 'minimum', 'mname', 'refresh', 'retry', 'serial' ],
        'SRV': ['port', 'priority', 'target', 'weight'],
        'MX': ['exchange', 'preference'],
        'NS': ['target'],
        'CNAME': ['target'],
        'TXT': ['strings'],
        'SPF': ['strings']
    }

    def __init__(self, **options):
        self.options = options

    def _do_axfr(self, domain):
        p =  dns.query.xfr(self.options.get('ipaddr', '127.0.0.1'), domain)
        return dns.zone.from_xfr(p)


    def get_zone(self, domain):

        zoned = self._do_axfr(domain)

        jsonzone = {}
        jsonzone[str(zoned.origin)] = {}

        for rtype in self.supp_types:
            jsonzone[str(zoned.origin)][rtype] = []

        for name, node in zoned.nodes.items():
            rdatasets = node.rdatasets
            for rdataset in rdatasets:

                rdata_text_repr = dns.rdatatype.to_text(rdataset.rdtype)

                lentry = {}
                lentry['ttl'] = rdataset.ttl
                lentry['host'] = str(name)

                for rdata in rdataset:

                    if rdata_text_repr in self.supp_types:
                        try:
                            for fname in self.field_names.get(rdata_text_repr):
                                lentry[fname] = str(getattr(rdata, fname))
                        except TypeError as p:
                            print(p)
                jsonzone[str(zoned.origin)][rdata_text_repr].append(lentry)

        return json.dumps(jsonzone)

