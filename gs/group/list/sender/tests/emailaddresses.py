# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2014 OnlineGroups.net and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
############################################################################
from __future__ import absolute_import, unicode_literals
from mock import patch, MagicMock
from unittest import TestCase
from gs.group.list.sender.emailaddresses import EmailPerPostAddresses


class TestEmailPerPostAddresses(TestCase):
    addrs = ['person@people.example.com', 'member@members.example.com',
             'individual@people.example.com', 'admin@members.example.com', ]

    @patch('gs.group.list.sender.emailaddresses.createObject')
    @patch('gs.group.list.sender.emailaddresses.AddressQuery')
    def test_addresses(self, AddressQuery, createObject):
        q = AddressQuery.return_value
        q.email_per_post_addresses.return_value = self.addrs

        eppa = EmailPerPostAddresses(MagicMock())
        r = eppa.addresses

        expected = sorted(self.addrs, key=lambda s: s[::-1])
        self.assertEqual(r, expected)

    @patch('gs.group.list.sender.emailaddresses.createObject')
    @patch('gs.group.list.sender.emailaddresses.AddressQuery')
    def test_addresses_dupe(self, AddressQuery, createObject):
        'Test that duplicate addresses are dropped'
        q = AddressQuery.return_value
        addrs = self.addrs + [self.addrs[0]]
        q.email_per_post_addresses.return_value = addrs

        eppa = EmailPerPostAddresses(MagicMock())
        r = eppa.addresses

        expected = sorted(self.addrs, key=lambda s: s[::-1])
        self.assertEqual(r, expected)
        self.assertNotEqual(len(r), len(addrs))

    @patch('gs.group.list.sender.emailaddresses.createObject')
    @patch('gs.group.list.sender.emailaddresses.AddressQuery')
    def test_addresses_not_an_email(self, AddressQuery, createObject):
        'Test that non-addresses are dropped'
        q = AddressQuery.return_value
        addrs = self.addrs + ['Parrot']
        q.email_per_post_addresses.return_value = addrs

        eppa = EmailPerPostAddresses(MagicMock())
        r = eppa.addresses

        expected = sorted(self.addrs, key=lambda s: s[::-1])
        self.assertEqual(r, expected)
        self.assertNotEqual(len(r), len(addrs))
