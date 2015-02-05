:mod:`gs.group.list.sender`
===========================

Contents:

.. toctree::
   :maxdepth: 2

   sender
   recipients
   headers
   standard
   HISTORY

This product provides the *Message sender* for a GroupServer_
group (see :doc:`sender`). When a post is added to a group it is
accepted, and archived. Then this product sends an email to every
group member that wishes to receive an email notification.

The email notification is *mostly* made up of the original post,
but the headers are highly modified (see :doc:`headers`). That
modification is the job of this product.

Once the messages are batched the recipients are determined (see
:doc:`recipients`), organised into batches, and then the email is
sent out using ``SMTP``.

Resources
=========

- Code repository: https://github.com/groupserver/gs.group.list.sender
- Questions and comments to http://groupserver.org/groups/development
- Report bugs at https://redmine.iopen.net/projects/groupserver

.. _GroupServer: http://groupserver.org/
