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
from gs.group.list.sender.headers.frm import FromHeader
from .faux import (FauxGroup, FauxRequest, get_email, )


class TestFromHeader(TestCase):
    'Test the From-header class'

    def test_rget_anon_address(self):
        fh = FromHeader(FauxGroup, FauxRequest)
        r = fh.get_anon_address('person', 'example.com',
                                'groups.example.com')
        self.assertEqual('anon-person-at-example-com@groups.example.com', r)
