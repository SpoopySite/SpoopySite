import dns.resolver
import dns.rrset
from dns.asyncresolver import Resolver
from dns.resolver import NXDOMAIN
import logging
import tld

log = logging.getLogger(__name__)


async def check(domain: str, rtype: str = "A") -> dns.rrset.RRset:
    log.info(f"CloudFlare checking: '{domain}'")
    if domain.count(":") > 0:
        processed_url = tld.get_fld(domain, fix_protocol=True)
        log.info(f"CloudFlare processed: '{domain}' to '{processed_url}'")
        domain = processed_url
    rs = Resolver()
    rs.nameservers = ["1.1.1.2"]
    rs.timeout = 5
    try:
        dns_res: dns.resolver.Answer = await rs.resolve(domain, rdtype=rtype)
    except NXDOMAIN:
        log.warning(f"Couldn't resolve: '{domain}'")
        return None
    return dns_res.rrset
