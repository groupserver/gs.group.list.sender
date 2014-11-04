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
from contextlib import contextmanager
from email.header import Header
from email.message import Message
from mock import patch
from unittest import TestCase
from zope.component import getGlobalSiteManager
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from gs.group.list.sender.modifyheaders import (modify_headers,
                                                HeaderModifier)
from gs.group.list.sender.interfaces import IEmailHeaderModifier
from .faux import (FauxGroup, IFauxGroup, get_email, FauxRequest,
                   FauxXMailer, UFauxXMailer, UTF8FauxXMailer)


class TestModifyHeadersFunction(TestCase):
    'Test the modify_headers function'

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


@contextmanager
def header_adapter(name, adapter):
    gsm = getGlobalSiteManager()
    gsm.registerAdapter(adapter, (IFauxGroup, IDefaultBrowserLayer),
                        IEmailHeaderModifier, name)
    yield
    gsm.unregisterAdapter(adapter, (IFauxGroup, IDefaultBrowserLayer),
                          IEmailHeaderModifier, name)


class TestHeaderModifier(TestCase):
    'Test the HeaderModifier class'

    def assertUnmodified(self, email, header, expected):
        'Assert a header in an email is unmodified'
        self.assertIn(header, email,
                      'The {} From header was dropped'.format(header))
        self.assertEqual(expected, email[header])

    def assertXMailer(self, email, expectedUnicode):
        'Assert the X-Mailer header is unmodified'
        self.assertIn('X-Mailer', email, 'The X-Mailer header is missing')
        expected = Header(expectedUnicode, 'utf-8').encode()
        self.assertEqual(expected, email['X-Mailer'])

    def test_no_modify(self):
        'Test that some headers are left as-is'
        hm = HeaderModifier(FauxGroup(), FauxRequest())
        e = get_email("Ce n'est pas un email'")

        with header_adapter('X-Mailer', FauxXMailer):
            hm.modify_headers(e)

        e2 = get_email("Ce n'est pas un email'")
        self.assertUnmodified(e, 'From', e2['From'])
        self.assertUnmodified(e, 'To', e2['To'])
        self.assertUnmodified(e, 'Subject', e2['Subject'])

    def test_add(self):
        'Test adding the fake X-Mailer header'
        hm = HeaderModifier(FauxGroup(), FauxRequest())
        e = get_email("Ce n'est pas un email'")

        with header_adapter('X-Mailer', FauxXMailer):
            hm.modify_headers(e)

        expected = FauxXMailer.modify_header(None)
        self.assertXMailer(e, expected)

    def test_modify(self):
        'Test modifying the fake X-Mailer header'
        hm = HeaderModifier(FauxGroup(), FauxRequest())
        e = get_email("Ce n'est pas un email'")
        e['X-Mailer'] = "Ce n'est pas un mailer'"

        with header_adapter('X-Mailer', FauxXMailer):
            hm.modify_headers(e)

        expected = FauxXMailer.modify_header(None)
        self.assertXMailer(e, expected)

    def test_add_unicode(self):
        'Test adding a fake X-Mailer header with Unicode'
        hm = HeaderModifier(FauxGroup(), FauxRequest())
        e = get_email("Ce n'est pas un email'")

        with header_adapter('X-Mailer', UFauxXMailer):
            hm.modify_headers(e)

        expected = UFauxXMailer.modify_header(None)
        self.assertXMailer(e, expected)

    def test_add_utf8(self):
        'Test adding a fake X-Mailer header if some UTF-8 slipped through'
        hm = HeaderModifier(FauxGroup(), FauxRequest())
        e = get_email("Ce n'est pas un email'")

        with header_adapter('X-Mailer', UTF8FauxXMailer):
            hm.modify_headers(e)

        expected = UTF8FauxXMailer.modify_header(None).decode('utf-8')
        self.assertXMailer(e, expected)
