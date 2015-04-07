# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2014, 2015 OnlineGroups.net and Contributors.
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
from .faux import (FauxGroup, FauxRequest, FauxGroupInfo, get_email,
                   FauxMailingListInfo)


class TestSubjectHeaders(TestCase):
    'Test the subject header class'

    @patch('gs.group.list.sender.headers.simpleadd.IGSGroupInfo')
    @patch('gs.group.list.sender.headers.simpleadd.IGSMailingListInfo')
    def test_title_short_name(self, IGSMailingListInfo, IGSGroupInfo):
        '''Test we return the short_name attribute in preference'''
        sh = SubjectHeader(FauxGroup, FauxRequest)
        IGSGroupInfo.return_value.get_property.side_effect = [
            'short name', 'another short name', 'group title']
        IGSGroupInfo.return_value.id = 'id'
        mlist = IGSMailingListInfo.return_value.mlist
        mlist.getProperty.return_value = 'mlist short name'

        r = sh.listTitle
        self.assertEqual(r, 'short name')

    @patch('gs.group.list.sender.headers.simpleadd.IGSGroupInfo')
    @patch('gs.group.list.sender.headers.simpleadd.IGSMailingListInfo')
    def test_title_shortName(self, IGSMailingListInfo, IGSGroupInfo):
        sh = SubjectHeader(FauxGroup, FauxRequest)
        IGSGroupInfo.return_value.get_property.side_effect = [
            None, 'another short name', 'group title']
        IGSGroupInfo.return_value.id = 'id'
        mlist = IGSMailingListInfo.return_value.mlist
        mlist.getProperty.return_value = 'mlist short name'

        r = sh.listTitle
        self.assertEqual(r, 'another short name')

    @patch('gs.group.list.sender.headers.simpleadd.IGSGroupInfo')
    @patch('gs.group.list.sender.headers.simpleadd.IGSMailingListInfo')
    def test_title_list(self, IGSMailingListInfo, IGSGroupInfo):
        sh = SubjectHeader(FauxGroup, FauxRequest)
        IGSGroupInfo.return_value.get_property.side_effect = [
            None, None, 'group title']
        IGSGroupInfo.return_value.id = 'id'
        mlist = IGSMailingListInfo.return_value.mlist
        mlist.getProperty.return_value = 'mlist short name'

        r = sh.listTitle
        self.assertEqual(r, 'mlist short name')

    @patch('gs.group.list.sender.headers.simpleadd.IGSGroupInfo')
    @patch('gs.group.list.sender.headers.simpleadd.IGSMailingListInfo')
    def test_title_group(self, IGSMailingListInfo, IGSGroupInfo):
        sh = SubjectHeader(FauxGroup, FauxRequest)
        IGSGroupInfo.return_value.get_property.side_effect = [
            None, None, 'group title']
        IGSGroupInfo.return_value.id = 'id'
        mlist = IGSMailingListInfo.return_value.mlist
        mlist.getProperty.return_value = None

        r = sh.listTitle
        self.assertEqual(r, 'group title')

    @patch('gs.group.list.sender.headers.simpleadd.IGSGroupInfo')
    @patch('gs.group.list.sender.headers.simpleadd.IGSMailingListInfo')
    def test_title_id(self, IGSMailingListInfo, IGSGroupInfo):
        sh = SubjectHeader(FauxGroup, FauxRequest)
        IGSGroupInfo.return_value.get_property.side_effect = [
            None, None, None]
        IGSGroupInfo.return_value.id = 'id'
        mlist = IGSMailingListInfo.return_value.mlist
        mlist.getProperty.return_value = None

        r = sh.listTitle
        self.assertEqual(r, 'id')

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

    @patch('gs.group.list.sender.headers.simpleadd.IGSGroupInfo')
    @patch('gs.group.list.sender.headers.simpleadd.IGSMailingListInfo')
    def test_group_name_add(self, IGSMailingListInfo, IGSGroupInfo):
        'Ensure the group-name is added'
        IGSGroupInfo.return_value = FauxGroupInfo()
        IGSMailingListInfo.return_value = FauxMailingListInfo()
        sh = SubjectHeader(FauxGroup, FauxRequest)
        e = get_email('I am a fish')

        r = sh.modify_header(e)
        self.assertEqual('[faux] I am a fish', r)

    @patch('gs.group.list.sender.headers.simpleadd.IGSGroupInfo')
    @patch('gs.group.list.sender.headers.simpleadd.IGSMailingListInfo')
    def test_group_name_add_once(self, IGSMailingListInfo, IGSGroupInfo):
        'Ensure the group-name is added once only'
        IGSGroupInfo.return_value = FauxGroupInfo()
        IGSMailingListInfo.return_value = FauxMailingListInfo()
        sh = SubjectHeader(FauxGroup, FauxRequest)
        e = get_email('[faux] I am a fish')

        r = sh.modify_header(e)
        self.assertEqual('[faux] I am a fish', r)

    @patch('gs.group.list.sender.headers.simpleadd.IGSGroupInfo')
    @patch('gs.group.list.sender.headers.simpleadd.IGSMailingListInfo')
    def test_group_name_add_re(self, IGSMailingListInfo, IGSGroupInfo):
        'Ensure the group-name is added when the Re is involved'
        IGSGroupInfo.return_value = FauxGroupInfo()
        IGSMailingListInfo.return_value = FauxMailingListInfo()
        sh = SubjectHeader(FauxGroup, FauxRequest)
        e = get_email('Re: I am a fish')

        r = sh.modify_header(e)
        self.assertEqual('Re: [faux] I am a fish', r)

    @patch('gs.group.list.sender.headers.simpleadd.IGSGroupInfo')
    @patch('gs.group.list.sender.headers.simpleadd.IGSMailingListInfo')
    def test_group_name_add_re_once(self, IGSMailingListInfo, IGSGroupInfo):
        'Ensure the group-name is added once when the Re is involved'
        IGSGroupInfo.return_value = FauxGroupInfo()
        IGSMailingListInfo.return_value = FauxMailingListInfo()
        sh = SubjectHeader(FauxGroup, FauxRequest)
        e = get_email('Re: [faux] I am a fish')

        r = sh.modify_header(e)
        self.assertEqual('Re: [faux] I am a fish', r)

    @patch('gs.group.list.sender.headers.simpleadd.IGSGroupInfo')
    @patch('gs.group.list.sender.headers.simpleadd.IGSMailingListInfo')
    def test_group_name_add_space(self, IGSMailingListInfo, IGSGroupInfo):
        'Ensure the group-name is added once when spaces are involved'
        IGSGroupInfo.return_value = FauxGroupInfo()
        IGSMailingListInfo.return_value = FauxMailingListInfo()
        sh = SubjectHeader(FauxGroup, FauxRequest)
        e = get_email('   [faux] I   am a fish')

        r = sh.modify_header(e)
        self.assertEqual('[faux] I am a fish', r)

    @patch('gs.group.list.sender.headers.simpleadd.IGSGroupInfo')
    @patch('gs.group.list.sender.headers.simpleadd.IGSMailingListInfo')
    def test_group_name_add_fwd(self, IGSMailingListInfo, IGSGroupInfo):
        'Ensure the group-name is added once when "Fwd:" is involved'
        IGSGroupInfo.return_value = FauxGroupInfo()
        IGSMailingListInfo.return_value = FauxMailingListInfo()
        sh = SubjectHeader(FauxGroup, FauxRequest)
        e = get_email('Fwd: I am a fish')

        r = sh.modify_header(e)
        self.assertEqual('[faux] I am a fish', r)

    @patch('gs.group.list.sender.headers.simpleadd.IGSGroupInfo')
    @patch('gs.group.list.sender.headers.simpleadd.IGSMailingListInfo')
    def test_group_name_add_fwd_bracket(self, IGSMailingListInfo,
                                        IGSGroupInfo):
        'Ensure the group-name is added once when "[Fwd: ]" is involved'
        IGSGroupInfo.return_value = FauxGroupInfo()
        IGSMailingListInfo.return_value = FauxMailingListInfo()
        sh = SubjectHeader(FauxGroup, FauxRequest)
        e = get_email('[Fwd: I am a fish]')

        r = sh.modify_header(e)
        self.assertEqual('[faux] I am a fish', r)

    @patch('gs.group.list.sender.headers.simpleadd.IGSGroupInfo')
    @patch('gs.group.list.sender.headers.simpleadd.IGSMailingListInfo')
    def test_group_name_add_fwd_re(self, IGSMailingListInfo, IGSGroupInfo):
        'Ensure the group-name is added once when "Fwd: Re:" is involved'
        IGSGroupInfo.return_value = FauxGroupInfo()
        IGSMailingListInfo.return_value = FauxMailingListInfo()
        sh = SubjectHeader(FauxGroup, FauxRequest)
        e = get_email('Fwd: Re: I am a fish')

        r = sh.modify_header(e)
        self.assertEqual('[faux] I am a fish', r)

    @patch('gs.group.list.sender.headers.simpleadd.IGSGroupInfo')
    @patch('gs.group.list.sender.headers.simpleadd.IGSMailingListInfo')
    def test_group_name_add_fwd_bracket_re(self, IGSMailingListInfo,
                                           IGSGroupInfo):
        'Ensure the group-name is added once when "[Fwd: Re: ]" is involved'
        IGSGroupInfo.return_value = FauxGroupInfo()
        IGSMailingListInfo.return_value = FauxMailingListInfo()
        sh = SubjectHeader(FauxGroup, FauxRequest)
        e = get_email('[Fwd: Re: I am a fish]')

        r = sh.modify_header(e)
        self.assertEqual('[faux] I am a fish', r)

    @patch('gs.group.list.sender.headers.simpleadd.IGSGroupInfo')
    @patch('gs.group.list.sender.headers.simpleadd.IGSMailingListInfo')
    def test_group_name_add_re_fwd_bracket(self, IGSMailingListInfo,
                                           IGSGroupInfo):
        'Ensure the group-name is added once when "Re: [Fwd: ]" is involved'
        IGSGroupInfo.return_value = FauxGroupInfo()
        IGSMailingListInfo.return_value = FauxMailingListInfo()
        sh = SubjectHeader(FauxGroup, FauxRequest)
        e = get_email('Re: [Fwd: I am a fish]')

        r = sh.modify_header(e)
        self.assertEqual('Re: [faux] I am a fish', r)

    @patch('gs.group.list.sender.headers.simpleadd.IGSGroupInfo')
    @patch('gs.group.list.sender.headers.simpleadd.IGSMailingListInfo')
    def test_sender(self, IGSMailingListInfo, IGSGroupInfo):
        '''Test the Sender header with a new subject'''
        IGSGroupInfo.return_value = FauxGroupInfo()
        IGSMailingListInfo.return_value = FauxMailingListInfo()

        sh = SubjectHeader(FauxGroup, FauxRequest)
        e = get_email('I am a fish')
        r = sh.modify_header(e)
        expected = '[faux] I am a fish'
        self.assertEqual(expected, r)

    @patch('gs.group.list.sender.headers.simpleadd.IGSGroupInfo')
    @patch('gs.group.list.sender.headers.simpleadd.IGSMailingListInfo')
    def test_sender_re(self, IGSMailingListInfo, IGSGroupInfo):
        '''Test the Sender header with an Re: subject'''
        IGSGroupInfo.return_value = FauxGroupInfo()
        IGSMailingListInfo.return_value = FauxMailingListInfo()

        sh = SubjectHeader(FauxGroup, FauxRequest)
        e = get_email('Re: I am a fish')
        r = sh.modify_header(e)
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
        e = get_email('[faux] I am a fish')
        r = sh.modify_header(e)
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
        e = get_email('Re: [faux] I am a fish')
        r = sh.modify_header(e)
        expected = 'Re: [faux] I am a fish'
        self.assertEqual(expected, r)
