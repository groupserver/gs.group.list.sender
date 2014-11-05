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
        retval = eppa.addresses()
        return retval

    def send(self, email):
        'Send the email to the group'
        e = modify_headers(email, self.group, self.request)
        mailString = e.as_string()
        send_email(self.returnpath, self.addresses, mailString)
