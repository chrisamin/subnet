"""
Module containing the form(s) for the subnet calculator.
"""
from __future__ import absolute_import

import socket

from django import forms
from django.utils import simplejson, safestring


class SubnetForm(forms.Form):
    """
    The main Django form for the subnet calculator, including the deductive 
    calculation logic.
    """
    address = forms.IPAddressField(required=False)
    hostname = forms.CharField(required=False)
    mask = forms.IPAddressField(required=False, label="Subnet (Mask)")
    cidr = forms.IntegerField(required=False, label="Subnet (CIDR)")
    num_hosts = forms.IntegerField(required=False)
    num_hosts.widget.attrs["readonly"] = "readonly"
    network = forms.IPAddressField(required=False, label="Subnet ID")
    first_host = forms.CharField(required=False)
    first_host.widget.attrs["readonly"] = "readonly"
    last_host = forms.CharField(required=False)
    last_host.widget.attrs["readonly"] = "readonly"
    broadcast = forms.CharField(required=False)
    broadcast.widget.attrs["readonly"] = "readonly"

    exclusive_inputs = [
        ["mask", "cidr"],
        ["address", "network", "hostname"],
    ]
    exclusive_inputs_json = safestring.mark_safe(simplejson.dumps(
        exclusive_inputs))

    def clean(self):
        """
        Overridden clean() method which carries out the usual validation and
        normalization, but also fills in the gaps in network information based
        on the form's data.
        """
        self.data = self.get_network_information()
        return self.data

    @staticmethod
    def human_to_int(address):
        """
        Take a human-readable IPv4 address in dot notation and convert to an
        integer.
        """
        parts = address.split(".")
        binary_parts = [bin(int(part)).split("b")[-1].rjust(8, "0") for part in
            parts]
        as_binary = "".join(binary_parts)
        return int(as_binary, 2)

    @staticmethod
    def int_to_human(address):
        """
        Take an int representing an IPv4 and convert to the human-readable dot
        notation.

        Note: although this isn't necesarily to be used as a filter, it follows
        the Django convention of returning an empty string on malformed input.
        """
        if not isinstance(address, int):
            return ""
        as_binary = bin(address).split("b")[-1]
        as_binary = as_binary.rjust(32, "0")

        parts = [as_binary[start:start + 8] for start in range(0, 32, 8)]

        return ".".join(str(int(part.ljust(8, "0"), 2)) for part in parts)

    @staticmethod
    def get_num_hosts(cidr):
        """
        Return the number of hosts available to a subnet described in the CIDR
        notation (number of contiguous leading bits).

        Note: although this isn't necesarily to be used as a filter, it follows
        the Django convention of returning an empty string on malformed input.
        """
        if not isinstance(cidr, int):
            return ""
        return 2 ** (32 - cidr) - 2

    def get_network_information(self):
        """
        Return a dict containing the most comprehensive possible set of
        information about a particular network, given the current state of
        self.cleaned_data.
        """
        address = self.cleaned_data.get("address")
        network = self.cleaned_data.get("network")
        mask = self.cleaned_data.get("mask")
        cidr = self.cleaned_data.get("cidr")
        hostname = self.cleaned_data.get("hostname")

        if hostname:
            try:
                address = self.human_to_int(socket.gethostbyname(hostname))
            except socket.gaierror:
                address = ""
                hostname = ""
        elif address:
            try:
                hostname, aliaslist, ipaddrlist = socket.gethostbyaddr(address)
            except socket.herror:
                hostname = ""
            address = self.human_to_int(address)
        else:
            hostname = ""

        if isinstance(cidr, int):
            # Force CIDR number to be between 0 and 30, inclusive.
            cidr = max(0, cidr)
            cidr = min(30, cidr)
            mask = int(("1" * cidr).ljust(32, "0"), 2)
        elif mask:
            mask = self.human_to_int(mask)
            cidr = bin(mask).count("1")

        num_hosts = self.get_num_hosts(cidr)

        if address and isinstance(mask, int):
            network = address & mask
        elif network:
            network = self.human_to_int(network)

        if isinstance(network, int):
            first_host = network + 1
            last_host = network + num_hosts
            broadcast = network + num_hosts + 1
        else:
            network = None
            first_host = None
            last_host = None
            broadcast = None

        return ({
            "address": self.int_to_human(address),
            "broadcast": self.int_to_human(broadcast),
            "cidr": cidr,
            "first_host": self.int_to_human(first_host),
            "hostname": hostname,
            "last_host": self.int_to_human(last_host),
            "mask": self.int_to_human(mask),
            "network": self.int_to_human(network),
            "num_hosts": num_hosts,
        })
