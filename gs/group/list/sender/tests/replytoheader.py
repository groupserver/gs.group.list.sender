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
from gs.group.list.sender.replytoheader import (ReplyToHeader, ReplyTo)
from .faux import (FauxGroup, FauxRequest, )


class TestReplyToHeader(TestCase):
    'Test the reply-to header class'

    @patch('gs.group.list.sender.simpleadd.IGSMailingListInfo')
    def test_reply_to_sender(self, IGSMailingListInfo):
        gp = IGSMailingListInfo.return_value.get_property
        gp.return_value = 'sender'

        rth = ReplyToHeader(FauxGroup, FauxRequest)
        r = rth.replyTo
        self.assertEqual(ReplyTo.author, r)

    @patch('gs.group.list.sender.simpleadd.IGSMailingListInfo')
    def test_reply_to_both(self, IGSMailingListInfo):
        gp = IGSMailingListInfo.return_value.get_property
        gp.return_value = 'both'

        rth = ReplyToHeader(FauxGroup, FauxRequest)
        r = rth.replyTo
        self.assertEqual(ReplyTo.both, r)

    @patch('gs.group.list.sender.simpleadd.IGSMailingListInfo')
    def test_reply_to_group(self, IGSMailingListInfo):
        gp = IGSMailingListInfo.return_value.get_property
        gp.return_value = 'group'

        rth = ReplyToHeader(FauxGroup, FauxRequest)
        r = rth.replyTo
        self.assertEqual(ReplyTo.group, r)

    @patch('gs.group.list.sender.simpleadd.IGSMailingListInfo')
    def test_reply_to_group_none(self, IGSMailingListInfo):
        'Ensure that reply-to-group is the default'
        gp = IGSMailingListInfo.return_value.get_property
        gp.return_value = None

        rth = ReplyToHeader(FauxGroup, FauxRequest)
        r = rth.replyTo
        self.assertEqual(ReplyTo.group, r)

    @patch('gs.group.list.sender.simpleadd.IGSGroupInfo')
    @patch('gs.group.list.sender.simpleadd.IGSMailingListInfo')
    def test_modify_author(self, IGSMailingListInfo, IGSGroupInfo):
        gp = IGSMailingListInfo.return_value.get_property
        gp.side_effect = ['sender', 'faux@groups.example.com']

        rth = ReplyToHeader(FauxGroup, FauxRequest)
        r = rth.modify_header('person@example.com')

        self.assertEqual('person@example.com', r)

    @patch('gs.group.list.sender.simpleadd.IGSGroupInfo')
    @patch('gs.group.list.sender.simpleadd.IGSMailingListInfo')
    def test_modify_group(self, IGSMailingListInfo, IGSGroupInfo):
        gp = IGSMailingListInfo.return_value.get_property
        gp.side_effect = ['group', 'faux@groups.example.com']

        rth = ReplyToHeader(FauxGroup, FauxRequest)
        r = rth.modify_header('person@example.com')

        self.assertEqual('faux@groups.example.com', r)

    @patch('gs.group.list.sender.simpleadd.IGSGroupInfo')
    @patch('gs.group.list.sender.simpleadd.IGSMailingListInfo')
    def test_modify_both(self, IGSMailingListInfo, IGSGroupInfo):
        gp = IGSMailingListInfo.return_value.get_property
        gp.side_effect = ['both', 'faux@groups.example.com']

        rth = ReplyToHeader(FauxGroup, FauxRequest)
        r = rth.modify_header('person@example.com')

        self.assertEqual('person@example.com, faux@groups.example.com', r)