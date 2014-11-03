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
from email.message import Message
from mock import patch
from unittest import TestCase
from gs.group.list.sender.headers import (modify_headers, HeaderModifier)
from .faux import FauxGroup, get_email


class TestModifyHeadersFunction(TestCase):

    @patch.object(HeaderModifier, 'modify_headers')
    def test_str_to_str(self, mock_mh):
        'Test that we get a string back if we feed in a string'

        e = get_email("Ce n'est pas un email'")
        mock_mh.return_value = e

        eStr = e.as_string()
        r = modify_headers(eStr, FauxGroup(), None)

        self.assertEqual(type(eStr), type(r), 'Wrong type returned')

    @patch.object(HeaderModifier, 'modify_headers')
    def test_email_to_email(self, mock_mh):
        'Test that we get a string back if we feed in a string'

        e = get_email("Ce n'est pas un email'")
        mock_mh.return_value = e

        r = modify_headers(e, FauxGroup(), None)

        self.assertEqual(type(e), type(r), 'Wrong type returned')
        self.assertTrue(isinstance(r, Message), 'Wrong class returned')
