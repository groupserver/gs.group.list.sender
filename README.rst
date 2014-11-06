========================
``gs.group.list.sender``
========================
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Sending email messages from a GroupServer group
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Author: `Michael JasonSmith`_
:Contact: Michael JasonSmith <mpj17@onlinegroups.net>
:Date: 2014-11-05
:Organization: `GroupServer.org`_
:Copyright: This document is licensed under a
  `Creative Commons Attribution-Share Alike 4.0 International License`_
  by `OnlineGroups.net`_.

..  _Creative Commons Attribution-Share Alike 4.0 International License:
    http://creativecommons.org/licenses/by-sa/4.0/

Introduction
============

This product provides the *Message sender* for a GroupServer_
group. When a post is added to a group it is accepted, and
archived. Then this product sends an email to every group member
that wishes to receive an email notification.

The email notification is *mostly* made up of the original post,
but the headers are highly modified. That modification is the job
of this product.

Once the messages are batched the recipients are determined,
organised into batches, and then the email is sent out using
``SMTP`` [#gsemail]_


Modified
--------

The following headers are normally present in email messages, but
they are modified from what is normally present.

``From``
~~~~~~~~

The ``From`` address is the most complex modification. If the
**email provider of the author** has a DMARC setting [#gsdmarc]_
then the ``From`` address will be rewritten to either

* ``member-{userId}@{canonical-host}`` if the author has a profile,
  or
* ``anon-{mbox}-at-{host}@{domain}`` if there is no profile for
  the member.

``Subject``
~~~~~~~~~~~

The ``Subject`` header has the short group-name (also the title
of the mailing-list object) — in square-brackets and after the
``Re: ``, if present — added to the subject if the name is
missing.

``Reply-to``
~~~~~~~~~~~~

The ``Reply-to`` header determines who receives the replies
(along with some of the `List-*`_ headers, some of the time).
For a post from an **announcement** group the ``Reply-to`` is set
to the author, as few recipients of the message can post to the
group. For a post from a **discussion** group the value of the
``Reply-to`` depends on what the site-administrator set:

Group:
  The ``Reply-to`` is set to the email-address of the group (the
  default for a discussion group).

Author:
  The ``Reply-to`` is set the email-address of the author.

Both:
  The ``Reply-to`` contains both the email-address of the group
  and the email address of the author.

Recipients
==========

The ``gs.group.list.sender.emailaddresses.EmailPerPostAddresses``
class generates the list of recipient addresses. The recipients
of post is calculated as follows.

* For each member of the group that is receiving one email per
  post

  + Get the group-specific email addresses of the member

    - Get the preferred addresses if there is no group-specific
      addresses

  + Add those addresses to the list of recipient addresses.

Then reverse-sort the list, which groups people by email-address
provider. Finally, send out email messages in batches of 50 by
``gs.email`` [#gsemail]_.

Resources
=========

- Code repository: https://github.com/groupserver/gs.group.list.sender
- Questions and comments to http://groupserver.org/groups/development
- Report bugs at https://redmine.iopen.net/projects/groupserver

.. [#gsemail] The ``gs.email`` product does the actual sending to
              the SMTP server
              <https://github.com/groupserver/gs.email>
.. [#gsdmarc] The ``gs.dmarc`` product determines the DMARC
              setting of the host.
              <https://github.com/groupserver/gs.dmarc>

.. _GroupServer: http://groupserver.org/
.. _GroupServer.org: http://groupserver.org/
.. _OnlineGroups.Net: https://onlinegroups.net
.. _Michael JasonSmith: http://groupserver.org/p/mpj17

..  LocalWords:  DMARC github SMTP mailto DKIM
