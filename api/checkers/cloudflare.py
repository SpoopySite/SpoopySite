import dns.resolver
import dns.rrset
from dns.asyncresolver import Resolver
from dns.resolver import NXDOMAIN
import logging

log = logging.getLogger(__name__)


async def check(domain: str, rtype: str = "A") -> dns.rrset.RRset:
    log.info(f"CloudFlare checking: '{domain}'")
    rs = Resolver()
    rs.nameservers = ["1.1.1.2"]
    rs.timeout = 5
    try:
        dns_res: dns.resolver.Answer = await rs.resolve(domain, rdtype=rtype)
    except NXDOMAIN:
        log.warning(f"Couldn't resolve: '{domain}'")
        return None
    return dns_res.rrset
