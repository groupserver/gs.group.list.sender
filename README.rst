========================
``gs.group.list.sender``
========================
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Sending email messages from a GroupServer group
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Author: `Michael JasonSmith`_
:Contact: Michael JasonSmith <mpj17@onlinegroups.net>
:Date: 2014-11-02
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
but the headers_ are highly modified. That modification is the
job of this product.

Once the messages are batched the recipients_ are determined,
organised into batches, and then the email is sent out using
``SMTP`` [#gsemail]_

Headers
=======

Some headers are added_, while others are modified_.

Added
-----

The following headers are added to a message. They are normally
associated with mailing-list functionality, and are rarely
present in simple person-to-person email messages.

``List-*``
~~~~~~~~~~

There are six headers specific to mailing lists, which are
defined in `RFC 2369`_:

* ``List-Help``: How to get help. It points to the Help pages for
  the site.
* ``List-Unsubscribe``: The most important of the ``list-``
  headers, this header contains a ``mailto`` for the Unsubscribe
  command, to get a person out of a group.
* ``List-Subscribe``: A ``mailto`` for subscribing to the group.
* ``List-Post``: A ``mailto`` for posting to the group. Used by
  the *Reply* button in some email clients.
* ``List-Owner``: The email address of the support-group for the site.
* ``List-Archive``: The URL for the group.

.. _RFC 2369: https://tools.ietf.org/html/RFC2369

``Precedence``
~~~~~~~~~~~~~~

The ``Precedence`` header is set to ``Bulk``, indicating to email
providers that there is a jolly good reason they are seeing
multiple copies of the same message.

``Sender``
~~~~~~~~~~

The ``Sender`` header is set to the email-address of the group.

``X-Mailer``
~~~~~~~~~~~~

The ``X-Mailer`` header is a unofficial standard. It is set to
``GroupServer <http://groupserver.org/> (gs.group.list.send)``.

Modified
--------

The following headers are normally present in email messages, but
they are modified from what is normally present.

``From``
~~~~~~~~

The ``From`` address is the most complex modification. If the
**host of the author** of the email message has a DMARC setting
then the ``From`` address will be rewritten to the form
``user-{userId}@{canonical-host}`` [#gsdmarc]_.

``DKIM-Signature``
~~~~~~~~~~~~~~~~~~

Related to the ``From`` address rewriting because of DMARC, the
``DKIM-Signature`` header is dropped, if present.

``Subject``
~~~~~~~~~~~

The ``Subject`` header has the short group-name , in
square-brackets, added to the subject if the name is missing.

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

The recipients of post is calculated as follows.

* For each member of the group that is receiving one email per
  post

  + Get the group-specific email addresses of the member

    - Get the preferred addresses if there is no group-specific
      addresses

  + Add those addresses to the list of recipient addresses.

Then reverse-sort the list, which groups people by email-address
provider. Finally, send out email messages in batches of 50.

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
