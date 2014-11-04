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
from email.message import Message
from email.parser import Parser
from email.utils import parseaddr
import sys
from zope.component import getGlobalSiteManager
from gs.core import to_unicode_or_bust
from .interfaces import IEmailHeaderModifier


class HeaderModifier(object):
    '''Modify the headers

:param obj group: A group object.
:param request: An HTTP request.'''
    def __init__(self, group, request):

        self.context = self.group = group
        self.request = request

    def modify_headers(self, email):
        '''Set the headers in an email message to the "correct" values

:param email: The email message to modify.
:type email: :class:`email.message.Message`
:returns: Nothing'''

        # Hack.
        # TODO: Ponder
        email['Reply-To'] = parseaddr(email['From'])[1]

        gsm = getGlobalSiteManager()
        for name, adaptor in gsm.getAdapters((self.group, self.request),
                                             IEmailHeaderModifier):
            oldValue = to_unicode_or_bust(email.get(name))
            nv = adaptor.modify_header(oldValue)
            hv = Header(nv, 'utf-8')
            newValue = hv.encode()
            if name in email:
                email.replace_header(name, newValue)
            else:
                email.add_header(name, newValue)


STRING = basestring if (sys.version_info < (3, )) else str


def modify_headers(email, group, request):
    '''Modifiy the headers in an email message prior to sending

:param email: The email message to modify.
:type emaill: :class:`email.message.Message` or ``str``
:param obj group: The group that is sending the email.
:param obj request: The HTTP request that causes the email to be sent.
:returns: The modified email message.
:rtype: :class:`email.message.Message` or ``str``, depending on what was
        provided.'''
    if isinstance(email, Message):
        e = email
        fromString = False
    elif isinstance(email, STRING):
        p = Parser()
        e = p.parsestr(email)
        fromString = True
    else:
        m = 'email must be a string or a email.message.Message'
        raise TypeError(m)

    hm = HeaderModifier(group, request)
    hm.modify_headers(e)

    retval = e.as_string() if fromString else e
    return retval
