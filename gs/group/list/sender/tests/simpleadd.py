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
#from email.header import Header
#from email.message import Message
from unittest import TestCase
from gs.group.list.sender.simpleadd import Precedence
from .faux import (FauxGroup, FauxRequest)


class TestStaticHeaders(TestCase):
    'Test the headers that are static'

    def test_precedence(self):
        'Ensure the precedence header is static'
        p = Precedence(FauxGroup, FauxRequest)
        r = p.modify_header()
        self.assertEqual('bulk', r)

    def test_precedence_previous_data(self):
        'Ensure the precedence header ignores its argument'
        p = Precedence(FauxGroup, FauxRequest)
        r = p.modify_header('wibble')
        self.assertEqual('bulk', r)
