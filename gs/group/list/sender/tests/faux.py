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
from zope.component import getGlobalSiteManager
from email.parser import Parser
from zope.interface import Interface, implementer
from gs.group.list.sender.interfaces import IEmailHeaderModifier


class IFauxGroup(Interface):
    'This is not a group'


@implementer(IFauxGroup)
class FauxGroup(object):
    'This is not a group'


def get_email(subject):
    retval = Parser().parsestr(
        'From: <member@example.com>\n'
        'To: <group@example.com>\n'
        'Subject: {0}\n'
        '\n'
        'Body would go here\n'.format(subject))
    return retval


@implementer(IEmailHeaderModifier)
class FauxXMailer(object):

    def __init__(self, group, request):
        pass

    def modify_header(self, oldValue):
        return 'gs.group.list.sender.tests.faux.FauxXMailer'

gsm = getGlobalSiteManager()
gsm.registerAdapter(FauxXMailer, (IFauxGroup, ), IEmailHeaderModifier,
                    'X-Mailer')
