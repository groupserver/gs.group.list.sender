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
import sys
from zope.component import getGlobalSiteManager
from .interfaces import IEmailHeaderModifier


class HeaderModifier(object):
    '''Modify the headers

:param group: A group object.
:type group: :class:`gs.group.base.interfaces.IGSGroupMarker`
:param request: An HTTP request.
:type request: :class:`zope.publisher.interfaces.browser.IDefaultBrowserLayer`
'''
    def __init__(self, group, request):

        self.context = self.group = group
        self.request = request

    def modify_headers(self, email):
        '''Set the headers in an email message to the "correct" values

:param email: The email message to modify.
:type email: :class:`email.message.Message`
:returns: The modified email message.
:rtype: :class:`email.message.Message`

The :meth:`HeaderModifier.modify_headers` method acquires the
header-adaptors (which conform to the
:class:`.interfaces.IEmailHeaderModifier` interface). It then itterates
through the adaptors (one per header) and then modifies the :obj:`email`
based on the output of the header-adaptor:

``None``:
    The header is deleted.
``str``:
    The header is set to the string.
``unicode``:
    The output is encoded (using :class:`email.header.Header`) and the
    header is set to the string.
'''
        gsm = getGlobalSiteManager()
        for name, adaptor in gsm.getAdapters((self.group, self.request),
                                             IEmailHeaderModifier):
            nv = adaptor.modify_header(email)
            if nv is None:
                # From the email.message docs:
                #   No exception is raised if the named field isn't present
                #   in the headers.
                del(email[name])
            else:
                if type(nv) == bytes:  # == str in Python 2
                    newValue = nv
                else:  # Unicode
                    hv = Header(nv, 'utf-8')
                    newValue = hv.encode()
                if name in email:
                    email.replace_header(name, newValue)
                else:
                    email.add_header(name, newValue)
        return email


STRING = basestring if (sys.version_info < (3, )) else str


def modify_headers(email, group, request):
    '''Modifiy the headers in an email message prior to sending

:param email: The email message to modify.
:type emaill: :class:`email.message.Message` or ``str``
:param group: The group that is sending the email.
:type group: :class:`gs.group.base.interfaces.IGSGroupMarker`
:param request: The HTTP request that causes the email to be sent.
:type request: :class:`zope.publisher.interfaces.browser.IDefaultBrowserLayer`
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
    modifiedEmail = hm.modify_headers(e)

    retval = modifiedEmail.as_string() if fromString else modifiedEmail
    return retval
