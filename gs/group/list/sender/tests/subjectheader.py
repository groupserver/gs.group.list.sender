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

        subj = 'Ethel the Frog'
        r = sh.is_reply(subj)
        self.assertFalse(r)

    def test_is_reply_re(self):
        sh = SubjectHeader(FauxGroup, FauxRequest)

        subj = 'Re: Ethel the Frog'
        r = sh.is_reply(subj)
        self.assertTrue(r)

    def test_is_reply_re_lower(self):
        sh = SubjectHeader(FauxGroup, FauxRequest)

        subj = 're: Ethel the Frog'
        r = sh.is_reply(subj)
        self.assertTrue(r)

    def test_is_reply_re_end(self):
        sh = SubjectHeader(FauxGroup, FauxRequest)

        subj = 'Ethel the Frog re:'
        r = sh.is_reply(subj)
        self.assertFalse(r)

    @patch('gs.group.list.sender.headers.simpleadd.IGSGroupInfo')
    @patch('gs.group.list.sender.headers.simpleadd.IGSMailingListInfo')
    def assert_subject(self, expected, s, IGSMailingListInfo, IGSGroupInfo):
        'Ensure the group-name is added'
        IGSGroupInfo.return_value = FauxGroupInfo()
        IGSMailingListInfo.return_value = FauxMailingListInfo()
        sh = SubjectHeader(FauxGroup, FauxRequest)
        e = get_email(s)

        r = sh.modify_header(e)
        self.assertEqual(expected, r)

    def test_group_name_add(self):
        'Ensure the group-name is added'
        self.assert_subject('[faux] Ethel the Frog', 'Ethel the Frog')

    def test_group_name_add_once(self):
        'Ensure the group-name is added once only'
        self.assert_subject('[faux] Ethel the Frog',
                            '[faux] Ethel the Frog')

    def test_group_name_add_re(self):
        'Ensure the group-name is added when the Re is involved'
        self.assert_subject('Re: [faux] Ethel the Frog',
                            'Re: Ethel the Frog')

    def test_group_name_add_re_once(self):
        'Ensure the group-name is added once when the Re is involved'
        self.assert_subject('Re: [faux] Ethel the Frog',
                            'Re: [faux] Ethel the Frog')

    def test_group_name_add_space(self):
        'Ensure the group-name is added once when spaces are involved'
        self.assert_subject('[faux] Ethel the Frog',
                            '   [faux] Ethel   the Frog')

    def test_group_name_add_fwd(self):
        'Ensure the group-name is added once when "Fwd:" is involved'
        self.assert_subject('[faux] Ethel the Frog', 'Fwd: Ethel the Frog')

    def test_group_name_add_fwd_bracket(self):
        'Ensure the group-name is added once when "[Fwd: ]" is involved'
        self.assert_subject('[faux] Ethel the Frog',
                            '[Fwd: Ethel the Frog]')

    def test_group_name_add_fwd_re(self):
        'Ensure the group-name is added once when "Fwd: Re:" is involved'
        self.assert_subject('[faux] Ethel the Frog',
                            'Fwd: Re: Ethel the Frog')

    def test_group_name_add_fwd_bracket_re(self):
        'Ensure the group-name is added once when "[Fwd: Re: ]" is involved'
        self.assert_subject('[faux] Ethel the Frog',
                            '[Fwd: Re: Ethel the Frog]')

    def test_group_name_add_re_fwd_bracket(self):
        'Ensure the group-name is added once when "Re: [Fwd: ]" is involved'
        self.assert_subject('Re: [faux] Ethel the Frog',
                            'Re: [Fwd: Ethel the Frog]')

    def test_other_group_name(self):
        'Is the group-name is added when another group name is convolved?'
        self.assert_subject('[faux] [other] Ethel the Frog',
                            '[other] Ethel the Frog')

    def test_other_group_name_fwd(self):
        'Is the group-name is added when another group name is convolved?'
        self.assert_subject('[faux] [other] Ethel the Frog',
                            'Fw: [other] Ethel the Frog')

    def test_other_group_name_fwd_bracket(self):
        'Is the group-name is added when another group name is convolved?'
        self.assert_subject('[faux] [other] Ethel the Frog',
                            '[Fwd: [other] Ethel the Frog]')
