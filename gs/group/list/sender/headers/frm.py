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
from zope.component import createObject
from zope.cachedescriptors.property import Lazy
from gs.cache import cache
from gs.config import (Config, getInstanceId)
from gs.core import to_unicode_or_bust
from gs.dmarc import (lookup_receiver_policy, ReceiverPolicy)
from .simpleadd import SimpleAddHeader
UTF8 = 'utf-8'


class FromHeader(SimpleAddHeader):
    '''The :mailheader:`From` header, with DMARC avoidance

:param group: A group object.
:type group: :class:`gs.group.base.interfaces.IGSGroupMarker`
:param request: An HTTP request.
:type request:
    :class:`zope.publisher.interfaces.browser.IDefaultBrowserLayer`

DMARC causes issues for groups. Lists usually set the :mailheader:`From`
to the email address of the person who wrote the message (contrast to the
:mailheader:`Sender`, :class:`.simpleadd.Sender`). However, if a member uses
an email-address from a host that has a DMARC policy of either
``quarantine`` or ``reject`` then the email from the group will be dropped
by the recipients as spam [#gsdmarc]_.

To get around this the :mailheader:`From` header is rewritten if the
host has DMARC turned on.

.. [#gsdmarc] The ``gs.dmarc`` product determines the DMARC
              setting of the host.
              <https://github.com/groupserver/gs.dmarc>
'''
    actualPolicies = (ReceiverPolicy.quarantine, ReceiverPolicy.reject)

    @Lazy
    def config(self):
        instanceId = getInstanceId()
        retval = Config(instanceId)
        return retval

    @Lazy
    def relayAddressPrefix(self):
        self.config.set_schema('smtp', {'relay-address-prefix': str})
        ws = self.config.get('smtp', strict=False)
        retval = ws.get('relay-address-prefix', 'p-')
        return retval

    @staticmethod
    @cache('gs.group.list.sender.header.from.dmarc', lambda h: h, 7 * 60)
    def get_dmarc_policy_for_host(host):
        retval = lookup_receiver_policy(host)
        return retval

    def get_user(self, email):
        siteRoot = self.context.site_root()
        acl_users = siteRoot.acl_users
        retval = acl_users.get_userByEmail(email)
        return retval

    def get_user_address(self, user, domain):
        '''Get a fake address for a member of a group.

:param user: The user.
:type user: :class:`Products.CustomUserFolder.CustomUser`
:param unicode domain: The host of the group.
:returns: An email address of the form
          ``{RELAY_ADDRESS_PREFIX}-{userId}@{domain}``.
:rtype: unicode'''
        r = '{prefix}{userId}@{domain}'
        retval = r.format(prefix=self.relayAddressPrefix,
                          userId=user.getId(), domain=domain)
        return retval

    @staticmethod
    def get_anon_address(mbox, host, domain):
        '''Get a fake address for a person without a profile

:param unicode mbox: The mbox from the email address of the person.
:param unicode host: The host from the email address of the person.
:param unicode domain: The host of the group.
:returns: An email address of the form ``'anon-{mbox}-at-{host}@{domain}'``.
:rtype: unicode'''
        r = 'anon-{mbox}-at-{host}@{domain}'
        h = host.replace('.', '-')
        retval = r.format(mbox=mbox, host=h, domain=domain)
        return retval

    @staticmethod
    def set_formally_from(email):
        '''Create an :mailheader:`X-GS-Formerly-From`

:param email: The email message to modify.
:type email: :class:`email.message.Message`

For debugging the :mailheader:`From` address is copied to a new
:mailheader:`X-GS-Formerly-From` header. This is **a side effect** of
modifying the :mailheader:`From` header.
'''
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
        '''Generate the content for the :mailheader:`From` header if
the mail provider has DMARC on.

:param email: The email message to modify.
:type email: :class:`email.message.Message`
:returns: Either:

    * A new :mailheader:`From` address if the mail provider has a DMARC
      policy of ``quarantine`` or ``reject``. The address with be of the
      form returned by :meth:`FromHeader.get_user_address` if the person
      has a profile, or that returned by
      :meth:`FromHeader.get_anon_address` otherwise.

    * The existing :mailheader:`From` address in all other situations.

:rtype: bytes'''
        originalFromAddr = parseaddr(email['From'])
        try:
            origHost = originalFromAddr[1].split('@')[1]
        except IndexError as ie:
            m = 'Could not parse the From address\n{addr}\n{err}'
            msg = m.format(addr=originalFromAddr, err=ie)
            log.warning(msg)
            retval = email['From']
            return retval

        dmarcPolicy = self.get_dmarc_policy_for_host(origHost)

        if (dmarcPolicy in self.actualPolicies):
            self.set_formally_from(email)
            m = 'Rewriting From address <{0}> because of DMARC settings '\
                'for "{1}" ({2})'
            log.info(m.format(originalFromAddr[1], origHost, dmarcPolicy))

            user = self.get_user(originalFromAddr[1])
            listMailto = self.listInfo.get_property('mailto')
            domain = parseaddr(listMailto)[1].split('@')[1]
            if (user is not None):  # Create a new From using the user-ID
                newAddress = self.get_user_address(user, domain)
                log.info('Using user-address <{0}>'.format(newAddress))
            else:  # Create a new From using the old address
                mbox, host = parseaddr(originalFromAddr)[1].split('@')
                newAddress = self.get_anon_address(mbox, host, domain)
                log.info('Using anon-address <{0}>'.format(newAddress))
            assert newAddress, 'The new email address is not set.'

            fn = self.get_best_name(originalFromAddr[0], user)
            headerName = Header(fn, UTF8)
            encodedName = headerName.encode()

            retval = formataddr((encodedName, newAddress))
        else:  # No DMARC to speak of
            retval = email['From']
        return retval
