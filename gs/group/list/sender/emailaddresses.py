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
from zope.cachedescriptors.property import Lazy
from zope.component import createObject
from gs.group.member.base import get_group_userids
from .queries import AddressQuery


class EmailPerPostAddresses(object):
    '''The email addresses for the group-members who get one email per post

:param group: A group object.
:type group: :class:`gs.group.base.interfaces.IGSGroupMarker`'''
    def __init__(self, group):
        self.context = self.group = group

    @Lazy
    def groupInfo(self):
        retval = createObject('groupserver.GroupInfo', self.context)
        return retval

    @Lazy
    def siteInfo(self):
        retval = createObject('groupserver.SiteInfo', self.context)
        return retval

    @Lazy
    def memberIds(self):
        retval = get_group_userids(self.context, self.groupInfo)
        return retval

    @Lazy
    def query(self):
        retval = AddressQuery()
        return retval

    @Lazy
    def addresses(self):
        '''The list of addresses

:returns: The list of email addresses
:rtype: A list of strings

The addresses are for each of the group members that have
* Verified email addresses,
* Are on *one email per post*, and
* Have not been blacklisted.

Each address is guarinteed to appear only once, and they are sorted by
the **reverse string**, so all the addresses from the same domain are next
to each other.'''
        addrs = self.query.email_per_post_addresses(self.siteInfo.id,
                                                    self.groupInfo.id,
                                                    self.memberIds)
        # Ensure the addresses are unique, and vaugely valid
        cleanAddresses = set([a for a in addrs if (a and ('@' in a))])
        # Sort the email addresses by the mail host
        retval = sorted(cleanAddresses, key=lambda s: s[::-1])
        return retval

    def __len__(self):
        retval = len(self.addresses)
        return retval

    def __iter__(self):
        for address in self.addresses:
            yield address
