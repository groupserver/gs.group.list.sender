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
from gs.email import send_email
from Products.GSGroup.interfaces import IGSMailingListInfo
from .emailaddresses import EmailPerPostAddresses
from .modifyheaders import modify_headers


class Sender(object):
    '''Send an email message from a group

:param group: A group object.
:type group: :class:`gs.group.base.interfaces.IGSGroupMarker`
:param request: An HTTP request.
:type request:
    :class:`zope.publisher.interfaces.browser.IDefaultBrowserLayer`
'''
    def __init__(self, group, request):
        self.context = self.group = group
        self.request = request

    @property
    def returnpath(self):
        li = IGSMailingListInfo(self.group)
        retval = li.get_property('mailto')
        return retval

    @property
    def addresses(self):
        eppa = EmailPerPostAddresses(self.group)
        retval = eppa.addresses
        return retval

    def send(self, email):
        '''Send the email to the group

:param email: The email message to send
:type email: :class:`email.message.Message`

The message will be sent with the email-address for the group set as the
``return path``, and with the headers modified by
:func:`gs.group.list.sender.modify_headers`. The recipients are defined by
:class:`.emailaddresses.EmailPerPostAddresses`.
'''
        e = modify_headers(email, self.group, self.request)
        mailString = e.as_string()
        send_email(self.returnpath, self.addresses, mailString)
