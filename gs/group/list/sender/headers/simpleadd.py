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
from email.header import Header
from email.utils import formataddr
from zope.cachedescriptors.property import Lazy
from gs.core import to_unicode_or_bust
from Products.GSGroup.interfaces import (IGSGroupInfo, IGSMailingListInfo)
UTF8 = 'utf-8'


class SimpleAddHeader(object):
    '''A simple header that is added to an email message'''
    def __init__(self, group, request):
        self.group = self.context = group
        self.request = request

    @Lazy
    def groupInfo(self):
        retval = IGSGroupInfo(self.group)
        return retval

    @Lazy
    def listInfo(self):
        retval = IGSMailingListInfo(self.group)
        return retval


class Precedence(SimpleAddHeader):
    ''':mailheader:`Precedence` header

The :mailheader:`Precedence` header is only ever set to ``bulk``.
This is not actually a header that is set by any standard.'''

    @staticmethod
    def modify_header(*args):
        '''Modify the :mailheader:`Precedence` header.

:returns: ``bulk``
:rtype: unicode'''
        retval = 'bulk'
        return retval


class XMailer(SimpleAddHeader):
    '''Create a :mailheader:`X-Mailer` header

The :mailheader:`X-Mailer` header is only ever set to a constant
string. While undefined by any standard, it is expected to be in the email
headers.'''

    @staticmethod
    def modify_header(*args):
        '''Modify the :mailheader:`X-Mailer` header.

:returns: ``GroupServer <http://groupserver.org/> (gs.group.list.send)``
:rtype: unicode'''
        retval = 'GroupServer <http://groupserver.org/> '\
                 '(gs.group.list.send)'
        return retval


class Sender(SimpleAddHeader):
    '''Create a :mailheader:`Sender` header

Defined in :rfc:`5322#section-3.6.2`, the :mailheader:`Sender` is
set to the email address of the group.'''
    def modify_header(self, *args):
        '''Modify the :mailheader:`Sender` header.

:returns: The *mailbox* of the group (a display-name and an angle-address).
:rtype: str'''
        name = to_unicode_or_bust(self.groupInfo.name)
        h = Header(name, UTF8)
        headerName = h.encode()
        addr = self.listInfo.get_property('mailto')
        retval = formataddr((headerName, addr))
        return retval


class ListHelp(SimpleAddHeader):
    '''Create a :mailheader:`List-Help` header

The :mailheader:`List-Help` header is described in
:rfc:`2369#section-3.1`.'''
    def modify_header(self, *args):
        '''Modify the :mailheader:`List-Help` header.

:returns: The URL of the Help page for the site.
:rtype: unicode'''
        retval = '<{0}/help/>'.format(self.groupInfo.siteInfo.url)
        return retval


class ListUnsubscribe(SimpleAddHeader):
    '''Create a :mailheader:`List-Unsubscribe` header

The :mailheader:`List-Unsubscribe` header contains a ``mailto:`` URL that
points to the Unsubscribe email address, described in
:rfc:`2369#section-3.2`. This is a **very** important header, because
many email clients send an email to this address when people click the
:guilabel:`Spam` button.'''
    def modify_header(self, *args):
        '''Modify the :mailheader:`List-Unsubscribe` header.

:returns: A ``mailto`` URL with the group-address and the
          :mailheader:`Subject` set to ``Unsubscribe``.
:rtype: unicode'''
        name = to_unicode_or_bust(self.groupInfo.name)
        desc = 'Leave {0}'.format(name)

        emailAddr = self.listInfo.get_property('mailto')
        addr = 'mailto:{0}?Subject=Unsubscribe'.format(emailAddr)

        retval = formataddr((desc, addr))
        return retval


class ListSubscribe(SimpleAddHeader):
    '''A ``mailto:`` pointing to the Subscrbe email address, described
in `RFC 2369`_

.. _RFC 2369: https://tools.ietf.org/html/rfc2369#section-3.3'''
    def modify_header(self, *args):
        name = to_unicode_or_bust(self.groupInfo.name)
        desc = 'Join {0}'.format(name)

        emailAddr = self.listInfo.get_property('mailto')
        addr = 'mailto:{0}?Subject=Subscribe'.format(emailAddr)

        retval = formataddr((desc, addr))
        return retval


class ListPost(SimpleAddHeader):
    '''A ``mailto:`` pointing to the email address for the group, described
in `RFC 2369`_

.. _RFC 2369: https://tools.ietf.org/html/rfc2369#section-3.4'''
    def modify_header(self, *args):
        emailAddr = self.listInfo.get_property('mailto')
        retval = '<mailto:{0}>'.format(emailAddr)
        return retval


class ListOwner(SimpleAddHeader):
    '''A ``mailto:`` pointing to the email address for the support group,
described in `RFC 2369`_

.. _RFC 2369: https://tools.ietf.org/html/rfc2369#section-3.5'''
    def modify_header(self, *args):
        emailAddr = self.groupInfo.siteInfo.get_support_email()
        retval = '<mailto:{0}>'.format(emailAddr)
        return retval


class ListArchive(SimpleAddHeader):
    '''The URL for the group, described in `RFC 2369`_

.. _RFC 2369: https://tools.ietf.org/html/rfc2369#section-3.6'''
    def modify_header(self, *args):
        addr = self.groupInfo.url
        retval = '<{0}>'.format(addr)
        return retval
