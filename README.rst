========================
``gs.group.list.sender``
========================
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Sending email messages from a GroupServer group
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Author: `Michael JasonSmith`_
:Contact: Michael JasonSmith <mpj17@onlinegroups.net>
:Date: 2014-11-06
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


Resources
=========

- Documentation: See the ``docs`` folder in this product.
- Code repository: https://github.com/groupserver/gs.group.list.sender
- Questions and comments to http://groupserver.org/groups/development
- Report bugs at https://redmine.iopen.net/projects/groupserver

.. [#gsemail] The ``gs.email`` product does the actual sending to
              the SMTP server
              <https://github.com/groupserver/gs.email>

.. _GroupServer: http://groupserver.org/
.. _GroupServer.org: http://groupserver.org/
.. _OnlineGroups.Net: https://onlinegroups.net
.. _Michael JasonSmith: http://groupserver.org/p/mpj17

..  LocalWords:  DMARC github SMTP mailto DKIM
