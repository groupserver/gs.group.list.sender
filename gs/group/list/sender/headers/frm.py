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
from email.utils import (parseaddr, formataddr)
from logging import getLogger
log = getLogger('gs.group.list.sender.header.from')
from zope.cachedescriptors.property import Lazy
from zope.component import createObject
from gs.cache import cache
from gs.core import to_unicode_or_bust
from gs.dmarc import (lookup_receiver_policy, ReceiverPolicy)
from .simpleadd import SimpleAddHeader
UTF8 = 'utf-8'


class FromHeader(SimpleAddHeader):
    'The From header, with DMARC avoidance.'
    actualPolicies = (ReceiverPolicy.quarantine, ReceiverPolicy.reject)

    @staticmethod
    @cache('gs.group.list.sender.header.from.dmarc', lambda h: h, 7 * 60)
    def get_dmarc_policy_for_host(host):
        retval = lookup_receiver_policy(host)
        return retval

    @Lazy
    def acl_users(self):
        siteRoot = self.context.site_root()
        retval = siteRoot.acl_users
        return retval

    def get_user_address(self, user, domain):
        userInfo = createObject('groupserver.UserFromId', self.context,
                                user.getId())
        r = 'member-{userInfo.id}@{domain}'
        retval = r.format(userInfo=userInfo, domain=domain)
        return retval

    @staticmethod
    def get_anon_address(mbox, host, domain):
            r = 'anon-{mbox}-at-{host}@{domain}'
            h = host.replace('.', '-')
            retval = r.format(mbox=mbox, host=h, domain=domain)
            return retval

    def set_formally_from(self, email):
        "Set the old From header to 'X-gs-formerly-from'"
        originalFromAddr = parseaddr(email['From'])
        oldName = to_unicode_or_bust(originalFromAddr[0])
        oldHeaderName = Header(oldName, UTF8)
        oldEncodedName = oldHeaderName.encode()
        oldFrom = formataddr((oldEncodedName, originalFromAddr[1]))
        email.add_header('X-GS-Formerly-From', oldFrom)

    def get_best_name(self, origName, user):
        'Pick the "best" name, using length as a proxy for "best"'
        retval = to_unicode_or_bust(origName)
        if user:
            userInfo = createObject('groupserver.UserFromId', self.context,
                                    user.getId())
            if (len(userInfo.name) >= len(origName)):
                retval = to_unicode_or_bust(userInfo.name)
        return retval

    def modify_header(self, email):
        'Generate a new From header if the mail provider has DMARC on'
        originalFromAddr = parseaddr(email['From'])
        origHost = originalFromAddr[1].split('@')[1]
        dmarcPolicy = self.get_dmarc_policy_for_host(origHost)

        if (dmarcPolicy in self.actualPolicies):
            self.set_formally_from(email, origHost, dmarcPolicy)
            m = 'Rewriting From address <{0}> because of DMARC settings '\
                'for "{1}" ({2})'
            log.info(m.format(originalFromAddr[1], origHost, dmarcPolicy))

            user = self.acl_users.get_userByEmail(originalFromAddr[1])
            listMailto = self.listInfo.get_property('mailto')
            domain = parseaddr(listMailto)[1].split('@')[1]
            if (user is not None):  # Create a new From using the user-ID
                newAddress = self.get_user_address(user, domain)
                log.info('Using user-address <{0}>'.format(newAddress))
            else:  # Create a new From using the old address
                mbox, host = parseaddr(originalFromAddr)[1].split('@')
                newAddress = self.get_anon_address(mbox, host, domain)
                log.info('Using anon-address <{0}>'.format(newAddress))
            assert(newAddress, 'The new email address is not set.')

            fn = self.get_best_name(originalFromAddr[0], user)
            headerName = Header(fn, UTF8)
            encodedName = headerName.encode()

            retval = formataddr((encodedName, newAddress))
        else:  # No DMARC to speak of
            retval = email['From']
        return retval
