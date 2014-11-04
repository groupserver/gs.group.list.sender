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
from email.parser import Parser
from zope.interface import Interface, implementer
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from gs.group.list.sender.interfaces import IEmailHeaderModifier


class IFauxGroup(Interface):
    'This is not a group'


@implementer(IFauxGroup)
class FauxGroup(object):
    'This is not a group'


class FauxSiteInfo(object):
    name = 'Faux Site'
    url = 'http://groups.example.com'

    def get_support_email(*args):
        return 'support@groups.example.com'


class FauxGroupInfo(object):
    name = 'Faux Group'
    url = 'http://groups.example.com/groups/faux'
    siteInfo = FauxSiteInfo()


class FauxMailingListInfo(object):
    def get_property(self, *args):
        return 'faux@groups.example.com'


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
    'The fake X-Mailer header modifier'

    def __init__(self, group, request):
        pass

    @staticmethod
    def modify_header(oldValue):
        return 'gs.group.list.sender.tests.faux.FauxXMailer'


@implementer(IEmailHeaderModifier)
class UFauxXMailer(FauxXMailer):
    @staticmethod
    def modify_header(oldValue):
        return '\u1F604'


@implementer(IEmailHeaderModifier)
class UTF8FauxXMailer(FauxXMailer):
    @staticmethod
    def modify_header(oldValue):
        return '\u1F604'.encode('utf-8')


@implementer(IDefaultBrowserLayer)
class FauxRequest(object):
    'This is not a request'
