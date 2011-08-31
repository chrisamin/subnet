import socket

from django.shortcuts import render_to_response
from django.template import RequestContext

from subnet import forms


def index(request, template_name="subnet/index.html"):
    if request.method == "POST":
        data = request.POST
    else:
        data = {
            "address": request.META.get("REMOTE_ADDR", "127.0.0.1"),
            "cidr": 0,
        }
        
    form = forms.SubnetForm(data)
    if form.is_valid():
        data = dict((key, value) for key, value in data.items())
        data.update(calculate(form.cleaned_data))
        form = forms.SubnetForm(data)

    context = {
        "form": form,
        }
    return render_to_response(template_name, context,
        context_instance=RequestContext(request))


def human_to_int(address):
    parts = address.split(".")
    binary_parts = [bin(int(part)).split("b")[-1].rjust(8, "0") for part in
        parts]
    as_binary = "".join(binary_parts)
    return int(as_binary, 2)


def int_to_human(address):
    if not isinstance(address, int):
        return ""
    prefix, as_binary = bin(address).split("b")
    as_binary = as_binary.rjust(32, "0")

    parts = [as_binary[start:start + 8] for start in range(0, 32, 8)]

    return ".".join(str(int(part.ljust(8, "0"), 2)) for part in parts)


def get_num_hosts(subnet):
    if not isinstance(subnet, int):
        return ""
    return 2 ** (32 - subnet) - 2


def calculate(data):
    address = data.get("address")
    network = data.get("network")
    mask = data.get("mask")
    cidr = data.get("cidr")
    hostname = data.get("hostname")

    if cidr < 0:
        cidr = 0
    if cidr > 30:
        cidr = 30

    if hostname:
        try:
            address = human_to_int(socket.gethostbyname(hostname))
        except socket.gaierror:
            address = ""
            hostname = ""
    elif address:
        try:
            hostname, aliaslist, ipaddrlist = socket.gethostbyaddr(address)
        except socket.herror:
            hostname = ""
        address = human_to_int(address)
    else:
        hostname = ""

    if isinstance(cidr, int):
        mask = int(("1" * cidr).ljust(32, "0"), 2)
    elif mask:
        mask = human_to_int(mask)
        cidr = bin(mask).count("1")

    num_hosts = get_num_hosts(cidr)

    if address and isinstance(mask, int):
        network = address & mask
    elif network:
        network = human_to_int(network)

    if isinstance(network, int):
        first_host = network + 1
        last_host = network + num_hosts
        broadcast = network + num_hosts + 1
    else:
        network = None
        first_host = None
        last_host = None
        broadcast = None

    return {
        "address": int_to_human(address),
        "broadcast": int_to_human(broadcast),
        "cidr": cidr,
        "first_host": int_to_human(first_host),
        "hostname": hostname,
        "last_host": int_to_human(last_host),
        "mask": int_to_human(mask),
        "network": int_to_human(network),
        "num_hosts": num_hosts,
    }
