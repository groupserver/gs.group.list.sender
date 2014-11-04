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
from enum import Enum
from zope.cachedescriptors.property import Lazy
from .simpleadd import SimpleAddHeader


class ReplyTo(Enum):
    '''An enumeration of the different reply-to settings.'''
    # __order__ is only needed in 2.x
    __order__ = 'author group both'

    #: The replies go to the author
    author = 0

    #: The replies go to the group
    group = 1

    #: The replies go to the author and the group
    both = 2


class ReplyToHeader(SimpleAddHeader):

    @Lazy
    def replyTo(self):
        r = self.listInfo.get_property('replyto', 'group')
        if r == 'sender':
            retval = ReplyTo.author
        elif r == 'both':
            retval = ReplyTo.both
        else:
            retval = ReplyTo.group
        return retval

    def modify_header(self, replyTo):
        if self.replyTo == ReplyTo.author:
            retval = replyTo
        elif self.replyTo == ReplyTo.group:
            retval = self.listInfo.get_property('mailto', replyTo)
        else:
            r = '{author}, {group}'
            retval = r.format(author=replyTo,
                              group=self.listInfo.get_property('mailto'))
        return retval
