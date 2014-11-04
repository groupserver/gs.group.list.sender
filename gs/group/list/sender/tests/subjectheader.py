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
from gs.group.list.sender.headers.subject import (SubjectHeader)
from .faux import (FauxGroup, FauxRequest, FauxGroupInfo,
                   FauxMailingListInfo)


class TestSubjectHeaders(TestCase):
    'Test the subject header class'
    def test_is_reply_no_re(self):
        sh = SubjectHeader(FauxGroup, FauxRequest)

        subj = 'I am a fish'
        r = sh.is_reply(subj)
        self.assertFalse(r)

    def test_is_reply_re(self):
        sh = SubjectHeader(FauxGroup, FauxRequest)

        subj = 'Re: I am a fish'
        r = sh.is_reply(subj)
        self.assertTrue(r)

    def test_is_reply_re_lower(self):
        sh = SubjectHeader(FauxGroup, FauxRequest)

        subj = 're: I am a fish'
        r = sh.is_reply(subj)
        self.assertTrue(r)

    def test_is_reply_re_end(self):
        sh = SubjectHeader(FauxGroup, FauxRequest)

        subj = 'I am a fish re:'
        r = sh.is_reply(subj)
        self.assertFalse(r)

    def test_strip_subject(self):
        sh = SubjectHeader(FauxGroup, FauxRequest)

        r = sh.strip_subject('[faux] I am a fish', 'faux')
        self.assertEqual('I am a fish', r)

    def test_strip_subject_missing(self):
        sh = SubjectHeader(FauxGroup, FauxRequest)

        r = sh.strip_subject('', 'faux')
        self.assertEqual('No subject', r)

    def test_strip_subject_space(self):
        sh = SubjectHeader(FauxGroup, FauxRequest)

        r = sh.strip_subject('   [faux] I   am a fish', 'faux')
        self.assertEqual('I am a fish', r)

    @patch('gs.group.list.sender.headers.simpleadd.IGSGroupInfo')
    @patch('gs.group.list.sender.headers.simpleadd.IGSMailingListInfo')
    def test_sender(self, IGSMailingListInfo, IGSGroupInfo):
        '''Test the Sender header with a new subject'''
        IGSGroupInfo.return_value = FauxGroupInfo()
        IGSMailingListInfo.return_value = FauxMailingListInfo()

        sh = SubjectHeader(FauxGroup, FauxRequest)
        r = sh.modify_header('I am a fish')
        expected = '[faux] I am a fish'
        self.assertEqual(expected, r)

    @patch('gs.group.list.sender.headers.simpleadd.IGSGroupInfo')
    @patch('gs.group.list.sender.headers.simpleadd.IGSMailingListInfo')
    def test_sender_re(self, IGSMailingListInfo, IGSGroupInfo):
        '''Test the Sender header with an Re: subject'''
        IGSGroupInfo.return_value = FauxGroupInfo()
        IGSMailingListInfo.return_value = FauxMailingListInfo()

        sh = SubjectHeader(FauxGroup, FauxRequest)
        r = sh.modify_header('Re: I am a fish')
        expected = 'Re: [faux] I am a fish'
        self.assertEqual(expected, r)

    @patch('gs.group.list.sender.headers.simpleadd.IGSGroupInfo')
    @patch('gs.group.list.sender.headers.simpleadd.IGSMailingListInfo')
    def test_sender_group(self, IGSMailingListInfo, IGSGroupInfo):
        '''Test the Sender header with a subject that contains the group
name already'''
        IGSGroupInfo.return_value = FauxGroupInfo()
        IGSMailingListInfo.return_value = FauxMailingListInfo()

        sh = SubjectHeader(FauxGroup, FauxRequest)
        r = sh.modify_header('[faux] I am a fish')
        expected = '[faux] I am a fish'
        self.assertEqual(expected, r)

    @patch('gs.group.list.sender.headers.simpleadd.IGSGroupInfo')
    @patch('gs.group.list.sender.headers.simpleadd.IGSMailingListInfo')
    def test_sender_group_re(self, IGSMailingListInfo, IGSGroupInfo):
        '''Test the Sender header with a subject that contains an Re: and
the group name'''
        IGSGroupInfo.return_value = FauxGroupInfo()
        IGSMailingListInfo.return_value = FauxMailingListInfo()

        sh = SubjectHeader(FauxGroup, FauxRequest)
        r = sh.modify_header('Re: [faux] I am a fish')
        expected = 'Re: [faux] I am a fish'
        self.assertEqual(expected, r)
