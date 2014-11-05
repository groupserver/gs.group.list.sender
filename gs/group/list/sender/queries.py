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
import sqlalchemy as sa
from gs.database import getTable, getSession


class AddressQuery(object):
    #: How many user ID's should we attempt to pass to the database before
    #: we just do the filtering ourselves to avoid the overhead on the
    #: database
    USER_FILTER_LIMIT = 255

    def __init__(self):
        self.emailSettingTable = getTable('email_setting')
        self.userEmailTable = getTable('user_email')
        self.groupUserEmailTable = getTable('group_user_email')
        self.emailBlacklist = getTable('email_blacklist')

    def members_on_digest_or_web(self, siteId, groupId):
        '''All the members with a setting that might include/exclude
        specific email addresses or block email delivery'''
        est = self.emailSettingTable
        s = est.select([est.c.user_id])
        # FIXME: See get_digest_addresses for why
        # email_settings.append_whereclause(est.c.site_id == site_id)
        s.append_whereclause(est.c.group_id == groupId)

        session = getSession()
        r = session.execute(s)

        retval = []
        if r.rowcount:
            for row in r:
                retval.append(row['user_id'])
        return retval

    def group_specific_addresses(self, siteId, groupId):
        guet = self.groupUserEmailTable
        uet = self.userEmailTable
        cols = [guet.c.user_id, guet.c.email]
        s = sa.select(cols)
        s.append_whereclause(guet.c.site_id == siteId)
        s.append_whereclause(guet.c.group_id == groupId)
        s.append_whereclause(guet.c.email == uet.c.email)
        s.append_whereclause(uet.c.verified_date != None)

        session = getSession()
        r = session.execute(s)
        retval = [{'user_id': x['user_id'],
                   'email': x['email']} for x in r]
        return retval

    def blacklist(self):
        eb = self.emailBlacklist
        s = eb.select()

        session = getSession()
        r = session.execute(s)

        retval = [row['email'].strip().lower() for row in r]
        return retval

    def email_per_post_addresses(self, siteId, groupId, memberIds):
        # TODO: We currently can't use site_id
        # preferred_only=True, process_settings=True, verified_only=True
        site_id = ''
        uet = self.userEmailTable
        retval = []

        ignoreIds = self.members_on_digest_or_web(site_id, groupId)

        specificUserAddresses = \
            self.group_specific_email_addresses(site_id, groupId)
        # Add the group-specific email address to the return value, and
        # ignore the remainder of the users.
        specificUsers = []
        for userId, address in specificUserAddresses:
            # Double check for security that this user should actually
            # be receiving email for this group.
            if ((userId in memberIds) and (userId not in ignoreIds)):
                specificUsers.append(userId)
                retval.append(address.lower())  # Why lower?
        ignoreIds += specificUsers  # Because they are now in retval

        # Remove any ids we have already processed
        userIds = [m for m in memberIds if m not in ignoreIds]
        # Get the list of banned addresses
        blacklistedAddresses = self.blacklist()

        s = uet.select()
        s.append_whereclause(uet.c.is_preferred == True)
        s.append_whereclause(uet.c.verified_date != None)
        if len(userIds) <= self.USER_FILTER_LIMIT:
            s.append_whereclause(uet.c.user_id.in_(userIds))

        session = getSession()
        r = session.execute(s)
        for row in r:
            e = row['email'].lower()
            if len(userIds) > self.USER_FILTER_LIMIT:
                if ((row['user_id'] in userIds)
                        and (e not in blacklistedAddresses)):
                    retval.append(e)
            elif (e not in blacklistedAddresses):
                retval.append(e)
        return retval
