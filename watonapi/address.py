import ipaddress

from dns import resolver
from dns.exception import DNSException
from . import errors

DEFAULT_PORT = 25565

def get_ip_port(full_address: str) -> (str, int):
    parts = full_address.split(':')
    if len(parts) > 2:
        raise errors.UnknownAddressError
    address = parts[0]
    port = parts[1] if len(parts) == 2 else None
    if _is_valid_ip(address):
        if not port:
            port = DEFAULT_PORT
        return address, port
    else:  # Its a domain name
        if not port:  # If it doesnt have a port try to find one using srv
            try:
                return _resolve_srv(address)
            except errors._NoSRVRecordError:
                port = DEFAULT_PORT
        return _resolve_a(address), port

def _is_valid_ip(ip: str) -> bool:
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def _resolve_srv(address: str) -> (str, int):
    try:
        records = resolver.resolve('_minecraft._tcp.'+address, 'SRV')
        if len(records) == 0:
            raise errors._NoSRVRecordError
        target_name = str(records[0].target).rstrip('.')
        target_ip = _resolve_a(target_name)
        return target_ip, records[0].port
    except DNSException:
        raise errors._NoSRVRecordError

def _resolve_a(address: str) -> str:
    try:
        records = resolver.resolve(address)
        return records[0].address
    except DNSException:
        raise errors.UnknownAddressError
