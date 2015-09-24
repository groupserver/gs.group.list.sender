# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2014, 2015 OnlineGroups.net and Contributors.
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
from email.utils import parseaddr
from gs.group.list.base import (replyto, ReplyTo)
from .simpleadd import SimpleAddHeader


class ReplyToHeader(SimpleAddHeader):
    '''The :mailheader:`Reply-To` header

:param group: A group object.
:type group: :class:`gs.group.base.interfaces.IGSGroupMarker`
:param request: An HTTP request.
:type request: :class:`zope.publisher.interfaces.browser.IDefaultBrowserLayer`

Group administrators sometimes want replies to email messages from a group
to go to odd places. This class sets the :mailheader:`Reply-To` header to
best reflect these odd views.'''

    def modify_header(self, email):
        '''Generate the content for the :mailheader:`Reply-To` header

:param email: The email message to modify.
:type email: :class:`email.message.Message`
:returns: Either:

    * The email address from the :mailheader:`From` header if the
      ``replyto`` property of the list-object is set to ``sender``. This is
      the default for announcement groups, as few group members can post to
      the group.
    * Both the email-address in the :mailheader:`From` header and the
      email-address of the group if the ``replyto`` property of the
      list-object is set to ``both``. (Yes, the :mailheader:`Reply-To`
      header can contain an *address-list* according to
      :rfc:`5322#section-3.6.2`.)
    * The email address for the group in all other cases. This is the
      default for most groups.

:rtype: bytes'''
        authorReplyTo = parseaddr(email.get('Reply-To',
                                  email.get('From')))[1]
        groupReplyTo = parseaddr(self.listInfo.get_property('mailto'))[1]
        replyTo = replyto(self.listInfo)
        if replyTo == ReplyTo.author:
            retval = authorReplyTo
        elif replyTo == ReplyTo.both:
            addrs = [a for a in [authorReplyTo, groupReplyTo] if a]
            retval = ', '.join(addrs)
        else:  # ReplyTo.group
            retval = groupReplyTo
        return retval
