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
from mock import patch
from unittest import TestCase
from gs.group.list.sender.headers.simpleadd import (
    Precedence, XMailer, Sender, ListUnsubscribe, ListHelp, ListSubscribe,
    ListPost, ListOwner, ListArchive)
from .faux import (FauxGroup, FauxRequest, FauxGroupInfo,
                   FauxMailingListInfo)


class TestStaticHeaders(TestCase):
    'Test the headers that are static'

    def test_precedence(self):
        'Ensure the precedence header is static'
        p = Precedence(FauxGroup, FauxRequest)
        r = p.modify_header()
        self.assertEqual('list', r)

    def test_precedence_previous_data(self):
        'Ensure the precedence header ignores its argument'
        p = Precedence(FauxGroup, FauxRequest)
        r = p.modify_header('wibble')
        self.assertEqual('list', r)

    def test_xmailer(self):
        'Test the X-Mailer header'
        xm = XMailer(FauxGroup, FauxRequest)
        r = xm.modify_header()
        expected = 'GroupServer <http://groupserver.org/> '\
                   '(gs.group.list.send)'
        self.assertEqual(expected, r)

    @patch('gs.group.list.sender.headers.simpleadd.IGSGroupInfo')
    @patch('gs.group.list.sender.headers.simpleadd.IGSMailingListInfo')
    def test_sender(self, IGSMailingListInfo, IGSGroupInfo):
        '''Test the Sender header'''
        IGSGroupInfo.return_value = FauxGroupInfo()
        IGSMailingListInfo.return_value = FauxMailingListInfo()

        s = Sender(FauxGroup, FauxRequest)
        r = s.modify_header()
        expected = 'Faux Group <faux@groups.example.com>'
        self.assertEqual(expected, r)

    @patch('gs.group.list.sender.headers.simpleadd.IGSGroupInfo')
    @patch('gs.group.list.sender.headers.simpleadd.IGSMailingListInfo')
    def test_list_help(self, IGSMailingListInfo, IGSGroupInfo):
        '''Test the ``List-Help`` header'''
        IGSGroupInfo.return_value = FauxGroupInfo()
        IGSMailingListInfo.return_value = FauxMailingListInfo()

        lh = ListHelp(FauxGroup, FauxRequest)
        r = lh.modify_header()
        expected = '<http://groups.example.com/help/>'
        self.assertEqual(expected, r)

    @patch('gs.group.list.sender.headers.simpleadd.IGSGroupInfo')
    @patch('gs.group.list.sender.headers.simpleadd.IGSMailingListInfo')
    def test_list_unsubscribe(self, IGSMailingListInfo, IGSGroupInfo):
        '''Test the ``List-Unsubscribe`` header'''
        IGSGroupInfo.return_value = FauxGroupInfo()
        IGSMailingListInfo.return_value = FauxMailingListInfo()

        lu = ListUnsubscribe(FauxGroup, FauxRequest)
        r = lu.modify_header()
        expected = 'Leave Faux Group '\
                   '<mailto:faux@groups.example.com?Subject=Unsubscribe>'
        self.assertEqual(expected, r)

    @patch('gs.group.list.sender.headers.simpleadd.IGSGroupInfo')
    @patch('gs.group.list.sender.headers.simpleadd.IGSMailingListInfo')
    def test_list_subscribe(self, IGSMailingListInfo, IGSGroupInfo):
        '''Test the ``List-Subscribe`` header'''
        IGSGroupInfo.return_value = FauxGroupInfo()
        IGSMailingListInfo.return_value = FauxMailingListInfo()

        ls = ListSubscribe(FauxGroup, FauxRequest)
        r = ls.modify_header()
        expected = 'Join Faux Group '\
                   '<mailto:faux@groups.example.com?Subject=Subscribe>'
        self.assertEqual(expected, r)

    @patch('gs.group.list.sender.headers.simpleadd.IGSGroupInfo')
    @patch('gs.group.list.sender.headers.simpleadd.IGSMailingListInfo')
    def test_list_post(self, IGSMailingListInfo, IGSGroupInfo):
        '''Test the ``List-Post`` header'''
        IGSGroupInfo.return_value = FauxGroupInfo()
        IGSMailingListInfo.return_value = FauxMailingListInfo()

        lp = ListPost(FauxGroup, FauxRequest)
        r = lp.modify_header()
        expected = '<mailto:faux@groups.example.com>'
        self.assertEqual(expected, r)

    @patch('gs.group.list.sender.headers.simpleadd.IGSGroupInfo')
    @patch('gs.group.list.sender.headers.simpleadd.IGSMailingListInfo')
    def test_list_owner(self, IGSMailingListInfo, IGSGroupInfo):
        '''Test the ``List-Owner`` header'''
        IGSGroupInfo.return_value = FauxGroupInfo()
        IGSMailingListInfo.return_value = FauxMailingListInfo()

        lo = ListOwner(FauxGroup, FauxRequest)
        r = lo.modify_header()
        expected = '<mailto:support@groups.example.com>'
        self.assertEqual(expected, r)

    @patch('gs.group.list.sender.headers.simpleadd.IGSGroupInfo')
    @patch('gs.group.list.sender.headers.simpleadd.IGSMailingListInfo')
    def test_list_archive(self, IGSMailingListInfo, IGSGroupInfo):
        '''Test the ``List-Archive`` header'''
        IGSGroupInfo.return_value = FauxGroupInfo()
        IGSMailingListInfo.return_value = FauxMailingListInfo()

        la = ListArchive(FauxGroup, FauxRequest)
        r = la.modify_header()
        expected = '<http://groups.example.com/groups/faux>'
        self.assertEqual(expected, r)
