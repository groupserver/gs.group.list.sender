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
from zope.cachedescriptors.property import Lazy
from gs.core import to_unicode_or_bust
from gs.group.list.base import EmailMessage
from .simpleadd import SimpleAddHeader


class SubjectHeader(SimpleAddHeader):
    '''The :mailheader:`Subject` header, with the group name

:param group: A group object.
:type group: :class:`gs.group.base.interfaces.IGSGroupMarker`
:param request: An HTTP request.
:type request:
  :class:`zope.publisher.interfaces.browser.IDefaultBrowserLayer`

It is convinient to add the group-name to the :mailheader:`Subject` header
so recipients of the email message can easily identify posts from the
group. This adaptor adds the *short name* (the ``title`` of the list
object) to the :mailheader:`Subject` header if it is not already there.'''

    @Lazy
    def listTitle(self):
        '''The title of the list

        :returns: The title of the list
        :rtype: unicode

        The title of the list is defined as

        * The ``short_name`` of the group, or if that is not set

          + The ``shortName`` of the group, or if that is not set

            = The ``title`` of the mailing list, or if that is not set

              - The ``title`` of the group, or if that is not set

                o The ID of the group.'''

        t = (self.groupInfo.get_property('short_name', None)
             or self.groupInfo.get_property('shortName', None)
             or self.listInfo.mlist.getProperty('title', None)
             or self.groupInfo.get_property('title', None)
             or self.groupInfo.id)
        retval = to_unicode_or_bust(t)
        return retval

    def modify_header(self, email):
        '''Generate the content for the :mailheader:`Subject` header

:param email: The email message to modify.
:type email: :class:`email.message.Message`
:returns: The new value for the :mailheader:`Subject` header, which
          will contain the title of the mailing-list object in
          square-brackets.'''
        re = 'Re: ' if self.is_reply(email['Subject']) else ''
        em = EmailMessage(email.as_string(), self.listTitle,
                          self.groupInfo.id, self.groupInfo.siteInfo.id)
        r = '{re}[{groupName}] {subject}'
        retval = r.format(re=re, groupName=self.listTitle,
                          subject=em.subject)
        return retval

    @staticmethod
    def is_reply(subj):
        retval = ((len(subj) > 3)
                  and (subj.lower().find('re:', 0, 3)) == 0)
        return retval
