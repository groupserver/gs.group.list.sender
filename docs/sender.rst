Sender
======

The :class:`Sender` class sends an email message from a group.

.. autoclass:: gs.group.list.sender.Sender
   :members:

Email addresses
---------------

The recipients of the email message is defined by the
:class:`.emailaddresses.EmailPerPostAddresses` class.

.. autoclass:: gs.group.list.sender.emailaddresses.EmailPerPostAddresses
   :members: 

   .. py:attribute:: addresses

      The addresses are for each of the group members that have

      * Verified email addresses,
      * Are on *one email per post*, and
      * Have not been blacklisted.

      Each address is guarinteed to appear only once, and they
      are sorted by the **reverse string**, so all the
      addresses from the same domain are next to each other.
