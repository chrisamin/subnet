"""
Module containing various TestCases which test certain input/output pairings.
"""
from __future__ import absolute_import

from django.test import TestCase

from . import forms


class SubnetTestCase(TestCase):
    """
    TestCase which provides the basis for all the test cases below.
    """
    inputs = {}
    outputs = {}

    def test(self):
        form = forms.SubnetForm(self.inputs)
        self.assertTrue(form.is_valid())

        for output_key, output_value in self.outputs.items():
            actual_value = form.cleaned_data.get(output_key, "undefined")
            self.assertEquals(output_value, actual_value)


class TestCase1(SubnetTestCase):
    """
    TestCase for 192.168.0.0/16.
    """
    inputs = {
        "address": "192.168.0.1",
        "cidr": "16",
    }

    outputs = {
        "network": "192.168.0.0",
        "mask": "255.255.0.0",
        "first_host": "192.168.0.1",
        "last_host": "192.168.255.254",
        "broadcast": "192.168.255.255",
        "num_hosts": 65534,
    }


class TestCase2(SubnetTestCase):
    """
    TestCase for 172.16.0.0/12.
    """
    inputs = {
        "address": "172.16.0.1",
        "mask": "255.240.0.0",
        }

    outputs = {
        "cidr": 12,
        "network": "172.16.0.0",
        "first_host": "172.16.0.1",
        "last_host": "172.31.255.254",
        "broadcast": "172.31.255.255",
        "num_hosts": 1048574,
    }


class TestCase3(SubnetTestCase):
    """
    TestCase for 10.0.0.0/8
    """
    inputs = {
        "network": "10.0.0.0",
        "mask": "255.0.0.0",
    }

    outputs = {
        "cidr": 8,
        "first_host": "10.0.0.1",
        "last_host": "10.255.255.254",
        "broadcast": "10.255.255.255",
        "num_hosts": 16777214,
        "address": "",
    }
