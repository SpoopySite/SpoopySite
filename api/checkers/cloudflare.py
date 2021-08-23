import dns.resolver
import dns.rrset
from dns.asyncresolver import Resolver
import logging

log = logging.getLogger(__name__)


async def check(domain: str, rtype: str = "A") -> dns.rrset.RRset:
    log.info(f"CloudFlare checking: '{domain}'")
    rs = Resolver()
    rs.nameservers = ["1.1.1.2"]
    rs.timeout = 5
    dns_res: dns.resolver.Answer = await rs.resolve(domain, rdtype=rtype)
    return dns_res.rrset
