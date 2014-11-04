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
from re import (compile as re_compile, sub, escape)
from string import whitespace
from gs.core import to_unicode_or_bust
from .simpleadd import SimpleAddHeader


class SubjectHeader(SimpleAddHeader):
    paraRegexep = re_compile('[\u2028\u2029]+')
    annoyingChars = whitespace + '\uFFF9\uFFFA\uFFFB\uFFFC\uFEFF'
    annoyingCharsL = annoyingChars + '\u202A\u202D'
    annoyingCharsR = annoyingChars + '\u202B\u202E'

    def modify_header(self, email):
        subject = email['Subject']
        listTitle = to_unicode_or_bust(self.groupInfo.get_property(
            'short_name', self.listInfo.mlist.title_or_id()))
        s = to_unicode_or_bust(subject)
        newSubj = self.strip_subject(s, listTitle)

        re = ''
        if self.is_reply(newSubj):
            newSubj = newSubj[3:].strip()
            re = 'Re: '

        r = '{re}[{groupName}] {subject}'
        retval = r.format(re=re, groupName=listTitle, subject=newSubj)
        return retval

    def strip_subject(self, subj, listTitle):
        '''Remove the list title from the subject, if it isn't just an empty
string'''
        if listTitle:
            elt = escape(listTitle)
            subject = sub('\[%s\]' % elt, '', subj).strip()

        subject = self.paraRegexep.sub(' ', subject)
        # compress up the whitespace into a single space
        subject = sub('\s+', ' ', subject).strip()
        subject = subject.lstrip(self.annoyingCharsL)
        subject = subject.rstrip(self.annoyingCharsR)

        if len(subject) <= 0:
            retval = 'No subject'
        else:
            retval = subject
        return retval

    @staticmethod
    def is_reply(subj):
        retval = ((len(subj) > 3)
                  and (subj.lower().find('re:', 0, 3)) == 0)
        return retval
