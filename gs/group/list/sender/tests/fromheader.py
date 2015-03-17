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
from email.utils import parseaddr
from mock import patch, MagicMock
from unittest import TestCase
from gs.dmarc import ReceiverPolicy
from gs.group.list.sender.headers.frm import FromHeader
from .faux import (FauxGroup, FauxRequest, get_email, FauxUserInfo)


class TestFromHeader(TestCase):
    'Test the From-header class'

    def test_get_anon_address(self):
        fh = FromHeader(FauxGroup, FauxRequest)
        r = fh.get_anon_address('person', 'example.com',
                                'groups.example.com')
        self.assertEqual('anon-person-at-example-com@groups.example.com', r)

    @patch.object(FromHeader, 'config')
    def test_get_user_address(self, configMock):
        configMock.get.return_value = {'relay-address-prefix': None}
        user = MagicMock()
        gid = user.getId
        gid.return_value = '0a1b2c3d'

        fh = FromHeader(FauxGroup, FauxRequest)
        r = fh.get_user_address(user, 'groups.example.com')
        self.assertEqual('p-0a1b2c3d@groups.example.com', r)

    def test_set_formally_from(self):
        e = get_email('Faux')
        fh = FromHeader(FauxGroup, FauxRequest)
        fh.set_formally_from(e)

        self.assertIn('X-GS-Formerly-From', e)
        f = parseaddr(e['From'])[1]
        ff = parseaddr(e['X-GS-Formerly-From'])[1]
        self.assertEqual(f, ff)

    def test_get_best_name_no_usr(self):
        'Get the best name when there is no user'
        fh = FromHeader(FauxGroup, FauxRequest)
        r = fh.get_best_name('A. B. Member', None)
        self.assertEqual('A. B. Member', r)

    @patch('gs.group.list.sender.headers.frm.createObject')
    def test_get_best_name_orig_long(self, createObject):
        'Get the best name when the original is the longest'
        u = FauxUserInfo()
        u.name = 'A. Member'
        createObject.return_value = u

        fh = FromHeader(FauxGroup, FauxRequest)
        r = fh.get_best_name('A. B. Member', MagicMock())
        self.assertEqual('A. B. Member', r)

    @patch('gs.group.list.sender.headers.frm.createObject')
    def test_get_best_name_usr_long(self, createObject):
        'Get the best name when the FN is the longest'
        u = FauxUserInfo()
        u.name = 'A. B. Member'
        createObject.return_value = u

        fh = FromHeader(FauxGroup, FauxRequest)
        r = fh.get_best_name('A. Member', MagicMock())
        self.assertEqual('A. B. Member', r)

    @patch('gs.group.list.sender.headers.frm.log')
    def test_from_missing(self, frmLog):
        'Cope with a missing From'
        e = get_email('Toad the wet sprocket')
        del(e['From'])
        fh = FromHeader(FauxGroup, FauxRequest)

        r = fh.modify_header(e)

        self.assertEqual(None, r)
        self.assertEqual(1, frmLog.warning.call_count)

    @patch.object(FromHeader, 'get_dmarc_policy_for_host')
    def test_dmarc_no_dmarc(self, gdpfh):
        'Test that everything is unmodified if there is no DMARC on'
        gdpfh.return_value = ReceiverPolicy.noDmarc

        fh = FromHeader(FauxGroup, FauxRequest)
        e = get_email('Faux')
        r = fh.modify_header(e)
        self.assertEqual(e['From'], r)

    @patch.object(FromHeader, 'get_dmarc_policy_for_host')
    def test_dmarc_none(self, gdpfh):
        'Test that everything is unmodified if the DMARC policy is ``none``'
        gdpfh.return_value = ReceiverPolicy.none

        fh = FromHeader(FauxGroup, FauxRequest)
        e = get_email('Faux')
        r = fh.modify_header(e)
        self.assertEqual(e['From'], r)

    def test_dmarc_reject_anon(self):
        '''Test that the address is rewritten for Anon when posting from a
domain controlled by DMARC-reject'''
        r, e = self.dmarc_modify_header(None, ReceiverPolicy.reject)

        self.assertIn('X-GS-Formerly-From', e)
        self.assertEqual(e['X-GS-Formerly-From'], 'member@example.com')
        self.assertEqual('anon-member-at-example-com@groups.example.com', r)

    @patch.object(FromHeader, 'config')
    def test_dmarc_reject_user(self, configMock):
        '''Test that the address is rewritten for a member when posting
from a domain controlled by DMARC-reject'''
        configMock.get.return_value = {'relay-address-prefix': None}
        user = MagicMock()
        user.getId.return_value = 'a0b1c2'
        r, e = self.dmarc_modify_header(user, ReceiverPolicy.reject)

        self.assertIn('X-GS-Formerly-From', e)
        self.assertEqual(e['X-GS-Formerly-From'], 'member@example.com')
        expected = '"A. B. Member" <p-a0b1c2@groups.example.com>'
        self.assertEqual(expected, r)

    def test_dmarc_quarantine_anon(self):
        '''Test that the address is rewritten for Anon when posting from a
domain controlled by DMARC-quarantine'''
        r, e = self.dmarc_modify_header(None, ReceiverPolicy.quarantine)

        self.assertIn('X-GS-Formerly-From', e)
        self.assertEqual(e['X-GS-Formerly-From'], 'member@example.com')
        self.assertEqual('anon-member-at-example-com@groups.example.com', r)

    @patch.object(FromHeader, 'config')
    def test_dmarc_quarantine_user(self, configMock):
        '''Test that the address is rewritten for a member when posting
from a domain controlled by DMARC-quarantine'''
        configMock.get.return_value = {'relay-address-prefix': None}
        user = MagicMock()
        user.getId.return_value = 'a0b1c2'
        r, e = self.dmarc_modify_header(user, ReceiverPolicy.quarantine)

        self.assertIn('X-GS-Formerly-From', e)
        self.assertEqual(e['X-GS-Formerly-From'], 'member@example.com')
        expected = '"A. B. Member" <p-a0b1c2@groups.example.com>'
        self.assertEqual(expected, r)

    @patch('gs.group.list.sender.headers.frm.createObject')
    @patch('gs.group.list.sender.headers.simpleadd.IGSGroupInfo')
    @patch('gs.group.list.sender.headers.simpleadd.IGSMailingListInfo')
    @patch.object(FromHeader, 'get_user')
    @patch.object(FromHeader, 'get_dmarc_policy_for_host')
    def dmarc_modify_header(self, user, dmarc, gdpfh, get_user,
                            IGSMailingListInfo, IGSGroupInfo, createObject):
        gdpfh.return_value = dmarc
        u = MagicMock()
        u.getId.return_value = 'a0b1c2'
        get_user.return_value = user
        IGSMailingListInfo.return_value.get_property.return_value = \
            'faux@groups.example.com'
        u = FauxUserInfo()
        u.name = 'A. B. Member'
        createObject.return_value = u

        fh = FromHeader(FauxGroup, FauxRequest)
        e = get_email('Faux')
        r = fh.modify_header(e)
        return (r, e)
